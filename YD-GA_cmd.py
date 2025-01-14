# coding: utf-8

import random
import re
import copy
import pandas as pd
#import matplotlib.pyplot as plt

jiBan = {
         '刺客':[2,4,6],
         '游侠':[2,3],
         '斗士':[2,4],
         '征服者':[2,4,6,8],
         '复苏者':[2,4],
         '神谕者':[2,4],
         '骑士':[2,4,6],
         '法师':[2,4],
         '神盾战士':[3,6],
         '秘术师':[2,3,4],
         '重骑兵':[2,3,4],
         '大魔王':[1],
         '神王':[1],
         '驯龙大师':[1],
         '破败军团':[3,6,9],
         '黑夜使者':[2,4,6,8],
         '魔女':[3],
         '小恶魔':[3,5,7],
         '屠龙勇士':[2,4],
         '丧尸':[2,3,4,5],
         '圣光卫士':[3,6,9],
         '黎明使者':[2,4,6,8],
         '神佑之森':[2,3],
         '龙族':[3,5],
         '铁甲卫士':[2,4],
         '永猎双子':[1],
         '复生亡魂':[2,3]
         }

shovel_add = ['神盾战士','破败军团','征服者','小恶魔','铁甲卫士','重骑兵','圣光卫士','复生亡魂','法师','屠龙勇士','复苏者','魔女','黎明使者','黑夜使者','刺客','丧尸']


def getHeroid(names, heros_info_short):
    '''
    输入英雄名称获得英雄id
    '''
    ids = []
    for name in names:
        if name in heros_info_short and heros_info_short[name] not in ids:
            ids.append(heros_info_short[name])
        else:
            print(name+ '不存在')
    return ids

def getHeroFromid(ids,heros_info):
    '''
    根据计算出的阵容返回英雄
    '''
    heros = []
    for i in ids:
        heros.append(heros_info['name'][i])
    return heros

def teamtype(hero_ids, heros_info):
    '''
    查看阵容,金币
    '''
    team = {}
    gold = 0
    for hero_id in hero_ids:
        gold += heros_info['gold'][hero_id]
        for job in heros_info['info'][hero_id]:
            if job in team:
                team[job] += 1
            else:
                team[job] = 1
    return team, gold

def calc(team, show= 0):
    '''
    计算队伍得分
    羁绊得分规则：按达成羁绊人数得分，不考虑羁绊效果不平衡（这是运营商的事!）
    '''
    score = 0
    for k in team:
            flag = 0#记录达成几人口羁绊
            if k != '忍者':
                pnum = team[k]
                for n in jiBan[k]:
                    if pnum >= n:
                        flag = n
                    else:
                        break
                #组成人口越多，得分越高
                score += flag**2
                if pnum >= jiBan[k][0] and show:
                    print('达成{}{}'.format(flag,k))
            elif team[k] == 1 or team[k] == 4:
                score += team[k]
                if show:
                    print('达成{}{}'.format(team[k],k))
            else:
                continue
    return score

def calculateTeamScore(team, show= 0, shovel= False):
    '''
    计算队伍得分(铲子)
    羁绊得分规则：按达成羁绊人数得分，不考虑羁绊效果不平衡（这是运营商的事!）
    '''
    max_score = 0
    if shovel:
    #计算铲子
        change = 'null'
        team_out = {}
        for j in shovel_add:
            #如果队伍里没有相关职业,跳过（铲子没有单独羁绊）
            if j not in team.keys():
                continue
            team_copy = copy.deepcopy(team)
            team_copy[j] +=1
            
            score = calc(team= team_copy, show= 0)
            change = change if score <= max_score else j
            team_out = team_out if score <= max_score else copy.deepcopy(team_copy)
            
            max_score = max_score if score <= max_score else score
        
        calc(team= team_out, show= show)
        return max_score, change
    else:
        max_score = calc(team= team, show= show)
        return max_score, None

def GA(team_pnum, selected_ids, heros_info, heros_info_short,gens = 2333, sample = 233, alpha = 0.1, shovel= False):
    '''
    team_pnum:你想组成多少人队伍
    selected_ids:列表,已经选定哪些英雄
    heros_info:英雄信息
    heros_info_short:英雄名称缩写信息
    gens:最大繁殖多少代
    sample:每代繁衍个体数
    alpha:金钱影响程度(值越大,越偏向便宜的英雄)
    '''
    selected_ids = getHeroid(selected_ids,heros_info_short= heros_info_short)
    
    hero_info_cp = copy.deepcopy(heros_info)
    k = len(selected_ids)
    n = team_pnum - k
    hero_couldchose = hero_info_cp['hero_id']
    
    for idxs in selected_ids:
        hero_couldchose.pop(hero_couldchose.index(idxs))
        
    #生成第一代
    scores = {
               'chosed_ids':[],
               'score':[]
              }
    for i in range(sample):
        hero_thisGenCouldChose = copy.deepcopy(hero_couldchose)
        random.shuffle(hero_thisGenCouldChose)
        teamChoesd =  selected_ids + hero_thisGenCouldChose[:n]
        team, gold = teamtype(teamChoesd, hero_info_cp)
        score,change = calculateTeamScore(team,shovel= shovel)
#         print('<================================>')
        score = score * 10 + gold * alpha if score > 0 else 0
        scores['chosed_ids'].append(teamChoesd)
        scores['score'].append(score)

    #开始繁衍
    maxscores = []
    for gen in range(gens):
        scores_thisgen = {
                           'chosed_ids':[],
                           'score':[]
                          }
        #最优的个体直接保存
        score_max_idx = scores['score'].index(max(scores['score']))
        scores_thisgen['chosed_ids'].append(scores['chosed_ids'][score_max_idx])
        scores_thisgen['score'].append(scores['score'][score_max_idx])
        
        #最差个体的直接重置掉（重复9次）
        for i in range(9):
            #重排、重选序号
            random.shuffle(hero_thisGenCouldChose)
            teamChoesd= selected_ids + hero_thisGenCouldChose[:n]
            #重新赋值
            score_min_idx = scores['score'].index(min(scores['score']))
            scores['chosed_ids'][score_min_idx] = teamChoesd
            scores_thisgen['chosed_ids'].append(teamChoesd)
            #计算得分
            team, gold = teamtype(teamChoesd, hero_info_cp)
            score,change = calculateTeamScore(team, shovel= shovel)
            score = score * 10 + gold * alpha if score > 0 else 0
            scores['score'][score_min_idx] = score
            scores_thisgen['score'].append(score)
        
        #计算累积概率
        p = [0]
        totalScores = sum(scores['score'])
        for i in range(2,sample):
            p.append(p[-1] + scores['score'][i]/totalScores)
            
        #根据轮盘赌法生成新一代个体
        for i in range(sample):
            #有莫名bug找不到双亲，所以先赋值，如果后面找到了会被覆盖
            Dad = scores['chosed_ids'][0]
            Mom = scores['chosed_ids'][-1]
            
            #选父体
            rnd = random.random()
            for theone in range(len(p)):
                if p[theone] > rnd:
                    Dad = scores['chosed_ids'][theone - 1]
                    break
                else:
                    continue
            #选母体
            rnd = random.random()
            for theone in range(len(p)):
                if p[theone] > rnd:
                    Mom = scores['chosed_ids'][theone - 1]
                    break
                else:
                    continue
            #求并集
            dadmon = list(set(Dad[k:]) | set(Mom[k:]))
            random.shuffle(dadmon)
            
            baby = selected_ids + dadmon[:n]
            #求得分
            team, gold = teamtype(baby, hero_info_cp)
            score,change = calculateTeamScore(team, shovel= shovel)
            score = score * 10 + gold * alpha if score > 0 else 0
            scores_thisgen['chosed_ids'].append(baby)
            scores_thisgen['score'].append(score)
        
        maxscores.append(max(scores_thisgen['score']))
        
        #保存这代信息
        scores = copy.deepcopy(scores_thisgen)
    
    #取出最佳个体
    besTeam = scores['chosed_ids'][scores['score'].index(max(scores['score']))]
    
    return besTeam, maxscores

def main(heros_list= [], team_pnum= 9, shovel = False, gens = 2333, sample = 233):
    '''
    hero_list: 你确定选的英雄
    team_pnum: 人口数
    gens：迭代次数（越高，越容易得到好的阵容但是运算时间久）
    sample：每代个体数（越高，越容易得到好的阵容但是运算时间久）
    '''
    #读取英雄信息
    heros_inf = pd.read_csv('data/heros_info.csv')
    heros_info = {col:heros_inf[col].tolist() for col in heros_inf.columns if col != 'info'}
    heros_info['info'] = []
    for i in range(len(heros_inf['info'])):
        heros_info['info'].append(re.findall(r'([\u4e00-\u9fa5]+)', heros_inf['info'][i]))
    heros_info_short = pd.read_csv('data/heros_info_short.csv')
    heros_info_short = {name:heros_info_short['hero_id'][i] for i, name in enumerate(heros_info_short['name'])}
    
    #计算
    besTeam, maxscores = GA(team_pnum= 9, 
                            selected_ids = heros_list, 
                            heros_info=heros_info,
                            heros_info_short= heros_info_short, 
                            gens = gens, 
                            sample = sample, 
                            alpha = 0.1,
                            shovel = shovel)

    team, gold = teamtype(besTeam, heros_info= heros_info)
    print(team)
    teamScore, change = calculateTeamScore(team= team, show = 1, shovel= shovel)
#     print(teamScore)
    if shovel:
        print('铲子变个{}'.format(change))
    heros = getHeroFromid(besTeam, heros_info= heros_info)
    print(heros)
    
#    plt.plot(list(range(gens)), maxscores, 'k.')
#    plt.rcParams['font.sans-serif']=['SimHei']
#    plt.rcParams['axes.unicode_minus'] = False
#    plt.xlabel('Gen', fontsize = 15)
#    plt.ylabel('Score', fontsize = 15)
#    plt.title('人工智障助手-云顶之弈', fontsize = 20, pad= 10)
#    plt.show()

if __name__ == '__main__':
    while(1):
        print('\n输入确定使用的英雄（空格隔开，不超过8）:')
        heros_list = input().split(' ')
        print('铲子增加一个羁绊？（默认不用，输入任意值使用）')
        shovel = bool(input())
        if shovel:
            print('已选择使用铲子')
        else:
            print('选择不使用铲子')
        print('=====计算中=====')
        main(heros_list= heros_list, team_pnum= 9, shovel = shovel, gens = 2333, sample = 233)