# -*- coding:utf-8 -*-
"""
第一版基于T5的摘要生成模型
"""

#from transformers import MT5ForConditionalGeneration
import jieba
from transformers import BertTokenizer, BatchEncoding
# from torch._six import container_abcs, string_classes, int_classes
import collections.abc as container_abcs

int_classes = int
string_classes = str

import torch
from torch.utils.data import DataLoader, Dataset
import re
import os
import csv
import argparse
from tqdm.auto import tqdm
from multiprocessing import Pool, Process
import pandas as pd
import numpy as np
import rouge

device = 'cuda' if torch.cuda.is_available() else 'cpu'
#print(device)
class T5PegasusTokenizer(BertTokenizer):
    """结合中文特点完善的Tokenizer
    基于词颗粒度的分词，如词表中未出现，再调用BERT原生Tokenizer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_tokenizer(self, x):
        return jieba.cut(x, HMM=False)

    def _tokenize(self, text, *arg, **kwargs):
        split_tokens = []
        for text in self.pre_tokenizer(text):
            if text in self.vocab:
                split_tokens.append(text)
            else:
                split_tokens.extend(super()._tokenize(text))
        return split_tokens

print("测试加载T5模型")
tokenizer_pre=T5PegasusTokenizer.from_pretrained('./WebPage/views/T5_Models/T5_trained_models/t5_pegasus_pretrain/chinese_t5_pegasus_small')
pre_model_abstract=torch.load('./WebPage/views/T5_Models/T5_trained_models/saved_model/abstract_model', map_location=device)
pre_model_title=torch.load('./WebPage/views/T5_Models/T5_trained_models/saved_model/summary_model', map_location=device)
print("加载文件")
class Opt:
    def __init__(self,
                 pretrained_model='./WebPage/views/T5_Models/T5_trained_models/t5_pegasus_pretrain/chinese_t5_pegasus_small',
                 model='./WebPage/views/T5_Models/T5_trained_models/saved_model/summary_model',
                 batch_size=16,
                 max_len=512,
                 max_len_generate=40,
                 use_multiprocess=False):

        self.pretrain_model=pretrained_model
        self.model=model
        self.batch_size=batch_size
        self.max_len=max_len
        self.max_len_generate=max_len_generate
        self.use_multiprocess=use_multiprocess

def predict_func(input_seq,model_path='./WebPage/views/T5_Models/T5_trained_models/saved_model/summary_model'):
    input_seq = [input_seq]

    def load_data(filename):
        """加载数据
        单条格式：(正文) 或 (标题, 正文)
        """
        D = []
        with open(filename, encoding='utf-8') as f:
            for l in f.readlines():
                cur = l.strip().split('\t')
                if len(cur) == 2:
                    title, content = cur[0], cur[1]
                    D.append((title, content))
                elif len(cur) == 1:
                    content = cur[0]
                    D.append(content)
        return D



    class KeyDataset(Dataset):
        def __init__(self, dict_data):
            self.data = dict_data

        def __len__(self):
            return len(self.data)

        def __getitem__(self, index):
            return self.data[index]

    def create_data(data, tokenizer, max_len):
        """调用tokenizer.encode编码正文/标题，每条样本用dict表示数据域
        """
        ret, flag, title = [], True, None
        for content in data:
            if type(content) == tuple:
                title, content = content
            text_ids = tokenizer.encode(content, max_length=max_len,
                                        truncation='only_first')

            if flag:
                flag = False
                #print(content)

            features = {'input_ids': text_ids,
                        'attention_mask': [1] * len(text_ids),
                        'raw_data': content}
            if title:
                features['title'] = title
            ret.append(features)
        return ret

    def sequence_padding(inputs, length=None, padding=0):
        """Numpy函数，将序列padding到同一长度
        """
        if length is None:
            length = max([len(x) for x in inputs])

        pad_width = [(0, 0) for _ in np.shape(inputs[0])]
        outputs = []
        for x in inputs:
            x = x[:length]
            pad_width[0] = (0, length - len(x))
            x = np.pad(x, pad_width, 'constant', constant_values=padding)
            outputs.append(x)

        return np.array(outputs, dtype='int64')

    def default_collate(batch):
        """组batch
        各个数据域分别转换为tensor，tensor第一个维度等于batch_size
        """
        np_str_obj_array_pattern = re.compile(r'[SaUO]')
        default_collate_err_msg_format = (
            "default_collate: batch must contain tensors, numpy arrays, numbers, "
            "dicts or lists; found {}")
        elem = batch[0]
        elem_type = type(elem)
        if isinstance(elem, torch.Tensor):
            out = None
            if torch.utils.data.get_worker_info() is not None:
                # If we're in a background process, concatenate directly into a
                # shared memory tensor to avoid an extra copy
                numel = sum([x.numel() for x in batch])
                storage = elem.storage()._new_shared(numel)
                out = elem.new(storage)
            return torch.stack(batch, 0, out=out).to(device)
        elif elem_type.__module__ == 'numpy' and elem_type.__name__ != 'str_' \
                and elem_type.__name__ != 'string_':
            if elem_type.__name__ == 'ndarray' or elem_type.__name__ == 'memmap':
                # array of string classes and object
                if np_str_obj_array_pattern.search(elem.dtype.str) is not None:
                    raise TypeError(default_collate_err_msg_format.format(elem.dtype))

                return default_collate([torch.as_tensor(b) for b in batch])
            elif elem.shape == ():  # scalars
                return torch.as_tensor(batch)
        elif isinstance(elem, float):
            return torch.tensor(batch, dtype=torch.float64)
        elif isinstance(elem, int_classes):
            return torch.tensor(batch, dtype=torch.long)
        elif isinstance(elem, string_classes):
            return batch
        elif isinstance(elem, container_abcs.Mapping):
            return {key: default_collate([d[key] for d in batch]) for key in elem}
        elif isinstance(elem, tuple) and hasattr(elem, '_fields'):  # namedtuple
            return elem_type(*(default_collate(samples) for samples in zip(*batch)))
        elif isinstance(elem, container_abcs.Sequence):
            # check to make sure that the elements in batch have consistent size
            it = iter(batch)
            elem_size = len(next(it))
            if not all(len(elem) == elem_size for elem in it):
                batch = sequence_padding(batch)

            return default_collate([default_collate(elem) for elem in batch])

        raise TypeError(default_collate_err_msg_format.format(elem_type))

    def prepare_data(args, tokenizer):
        """准备batch数据
        """
        test_data = input_seq
        test_data = create_data(test_data, tokenizer, args.max_len)
        test_data = KeyDataset(test_data)
        test_data = DataLoader(test_data, batch_size=args.batch_size, collate_fn=default_collate)
        return test_data

    def compute_rouge(source, target):
        """计算rouge-1、rouge-2、rouge-l
        """

        source, target = ' '.join(source), ' '.join(target)
        try:
            scores = rouge.Rouge().get_scores(hyps=source, refs=target)
            return {
                'rouge-1': scores[0]['rouge-1']['f'],
                'rouge-2': scores[0]['rouge-2']['f'],
                'rouge-l': scores[0]['rouge-l']['f'],
            }
        except ValueError:
            return {
                'rouge-1': 0.0,
                'rouge-2': 0.0,
                'rouge-l': 0.0,
            }

    def compute_rouges(sources, targets):
        scores = {
            'rouge-1': 0.0,
            'rouge-2': 0.0,
            'rouge-l': 0.0,
        }
        for source, target in zip(sources, targets):
            score = compute_rouge(source, target)
            for k, v in scores.items():
                scores[k] = v + score[k]

        return {k: v / len(targets) for k, v in scores.items()}

    def generate(test_data, model, tokenizer, args):
        gens, summaries = [], []
        # with open(args.result_file, 'w', encoding='utf-8', newline='') as f:
        #     writer = csv.writer(f, delimiter='\t')
        model.eval()
        for feature in tqdm(test_data):
            raw_data = feature['raw_data']
            content = {k: v for k, v in feature.items() if k not in ['raw_data', 'title']}
            gen = model.generate(max_length=args.max_len_generate,
                                 eos_token_id=tokenizer.sep_token_id,
                                 decoder_start_token_id=tokenizer.cls_token_id,
                                 **content)
            gen = tokenizer.batch_decode(gen, skip_special_tokens=True)
            gen = [item.replace(' ', '') for item in gen]
            # writer.writerows(zip(gen, raw_data))
            gens.extend(gen)
            if 'title' in feature:
                summaries.extend(feature['title'])
        if summaries:
            scores = compute_rouges(gens, summaries)
            print(scores)
        # print(gens[0])
        # print('生成结束！')
        return gens[0]

    def generate_multiprocess(feature):
        """多进程
        """
        model.eval()
        raw_data = feature['raw_data']
        content = {k: v for k, v in feature.items() if k != 'raw_data'}
        gen = model.generate(max_length=args.max_len_generate,
                             eos_token_id=tokenizer.sep_token_id,
                             decoder_start_token_id=tokenizer.cls_token_id,
                             **content)
        gen = tokenizer.batch_decode(gen, skip_special_tokens=True)
        results = ["{}\t{}".format(x.replace(' ', ''), y) for x, y in zip(gen, raw_data)]
        return results

    def init_argument():
        args=Opt(model=model_path)
        #todo:python的arg和Django会冲突，所以

        return args

    # if __name__ == '__main__':

    # step 1. init argument
    args = init_argument()

    # step 2. prepare test data
    print("文件位置：",args.pretrain_model)
    #tokenizer = T5PegasusTokenizer.from_pretrained(args.pretrain_model)
    tokenizer=tokenizer_pre
    test_data = prepare_data(args, tokenizer)

    # step 3. load finetuned model
    #model = torch.load(args.model, map_location=device)
    if(args.model=='./WebPage/views/T5_Models/T5_trained_models/saved_model/summary_model'):
        model=pre_model_title
    else:
        model=pre_model_abstract

    # step 4. predict
    res = []
    if args.use_multiprocess and device == 'cpu':
        print('Parent process %s.' % os.getpid())
        p = Pool(2)
        res = p.map_async(generate_multiprocess, test_data, chunksize=2).get()
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        res = pd.DataFrame([item for batch in res for item in batch])
        res.to_csv(args.result_file, index=False, header=False, encoding='utf-8')
        print('Done!')
    else:
        return generate(test_data, model, tokenizer, args)


#predict_func('美国作家托马斯·弗里德曼在畅销书《世界是平的》里描述了全球化进程及其给人们生活带来的巨大改变。然而，在即将过去的2019年，世界遭到逆全球化暗流的冲击，面临着治理、信任、和平和发展四大“赤字”的挑战。对此，弗里德曼2019年10月在接受采访时说，全球化没有好与坏，关键在于你如何掌控它。他过去三十年间多次来过中国，他说中国给他留下了深刻的印象。作为全球第二大经济体，中国2019年在维护经济全球化、削减全球四大“赤字”方面的努力，同样令世界印象深刻。2019年，气候变化、网络安全、难民危机等非传统安全威胁持续蔓延。个别国家为实现自身利益最大化，推行单边主义和贸易保护主义，冲击全球治理体系和多边机制。国际货币基金组织一年四次下调全球经济增长率至3%，这是2008年全球金融危机以来的最低水平；美欧等经济体国债收益率曲线出现倒挂，投资者的避险情绪正在蔓延。在这样的背景下，中国倡导的共商共建共享的全球治理观，可谓破解“治理赤字”的一剂良方。2019年，中国通过二十国集团、金砖峰会等多个国际合作平台，重申维护以联合国为核心的国际体系，努力构建更加公正合理的全球治理体系。中国共产党十九届四中全会明确提出，中国将积极参与全球治理体系的改革和建设，传递出坚定不移维护世界和平、促进共同发展的明确信号。治理赤字加剧的重要原因在于信任赤字的扩大。2019年，国际竞争摩擦日趋增多，国际社会信任和合作的基础受到侵蚀。信任是国际关系最好的黏合剂，破解信任赤字，需要加强不同文明间的交流对话。这一年，中国举办亚洲文明对话大会，为世界各国超越文明冲突与文明隔阂提供了有益借鉴，达成了普遍共识。2019年，地区冲突和局部战争持续不断，恐怖主义活动猖獗，和平赤字愈发突显。一些西方国家奉行“新干涉主义”，藉“人权”之名使用武力干涉他国内政，造成严重人道主义危机。近来，欧美社交网站掀起一股“十年挑战”风潮，许多网友通过照片对比晒出10年来的变化。然而，对于叙利亚、利比亚、伊拉克等战乱国家的网友来说，曾经的繁华因战火而凋零，他们晒出的是家破人亡的心酸和无奈。作为联合国安理会常任理事国，2019年中国参与了几乎所有国际和地区热点问题的解决进程，在朝鲜半岛核问题、阿富汗、叙利亚等问题上发挥了建设性作用。在这一年里，中国不仅参加国际反恐军事演习，更有超过2500名中国维和官兵坚守在全球多个战乱地区。目前，中国是安理会常任理事国中第一大出兵国，也是联合国维和行动的主要出资国。对此，联合国副秘书长阿图尔•哈雷评价说，中国在联合国维和行动中发挥着独特和关键作用，没有中国这样的会员国支持，联合国维和行动不可能取得今天这样的成就。需要指出的是，无论是破解治理赤字和信任赤字，还是破解和平赤字，归根到底，都离不开发展问题的解决。当前，国际社会对如何推进全球发展存在分歧。西方国家日益陷入发展模式困境，从“政治素人”的异军突起，到英国“脱欧”等“黑天鹅”事件层出不穷，上世纪80年代以来以“去监管化”为重要特征的新自由主义经济学加剧了南北发展的不平衡，也使得西方国家中产阶级规模持续缩小，造成民粹主义和民族主义回潮，弊端凸显，备受诟病。作为新兴经济体的重要代表，中国主张坚持公平包容，打造平衡普惠的发展模式，让世界各国人民共享经济全球化发展成果。这显然切合实际，符合国际社会共同利益。在这一理念指导下，中国在2019年继续推进“一带一路”倡议，为国际社会提供更多优质公共产品；举办第二届中国国际进口博览会，为各国生产商打开“机遇之门”。与此同时，中国在电商、人工智能、大数据、区块链等领域新技术的蓬勃发展，为破解发展赤字进行了新的探索和实践。在推选一个最能代表2019年国际形势的汉字时，中国人选了“难”这个字。虽然全球范围内的双边关系、多边关系和地区形势难题不断，但中国人仍将迎难而上，在攻坚克难中赢得新发展，为这个充满变数的世界注入更多确定性。')
