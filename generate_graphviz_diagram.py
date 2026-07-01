import os
import sys

graphviz_path = r'C:\Program Files\Graphviz\bin'
os.environ['PATH'] = graphviz_path + os.pathsep + os.environ.get('PATH', '')

import graphviz

dot = graphviz.Digraph('DSSAT草莓模型', comment='DSSAT草莓模型机理流程图', format='png')

dot.attr(rankdir='TB', size='24,20', dpi='300', fontname='Microsoft YaHei', fontsize='14')
dot.node_attr.update(shape='box', style='rounded,filled', fontname='Microsoft YaHei', fontsize='12')
dot.edge_attr.update(fontname='Microsoft YaHei', fontsize='10')

with dot.subgraph(name='cluster_input') as c:
    c.attr(label='输入模块', labeljust='l', fontsize='16', fontweight='bold', 
           color='#2c3e50', style='filled', fillcolor='#f8f9fa')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#3498db')
    c.node('species', '物种参数')
    c.node('variety', '品种参数')
    c.node('weather', '气象数据')
    c.node('management', '管理措施')
    c.node('soil', '土壤数据')

dot.node('daily_loop', '每日时间步长循环', style='filled', fillcolor='#3498db', color='#2980b9', fontcolor='white', fontsize='14')

with dot.subgraph(name='cluster_core') as c:
    c.attr(label='核心处理模块', labeljust='l', fontsize='16', fontweight='bold',
           color='#2c3e50', style='filled', fillcolor='#f8f9fa')
    
    with c.subgraph(name='cluster_env') as ce:
        ce.attr(label='环境驱动', labeljust='l', fontsize='14', fontweight='bold',
                color='#7f8c8d', style='filled', fillcolor='#ecf0f1')
        ce.node_attr.update(style='filled', fillcolor='#fff', color='#95a5a6')
        ce.node('met_process', '气象处理')
        ce.node('swd_dynamic', '土壤水氮动态')
    
    with c.subgraph(name='cluster_crop') as cc:
        cc.attr(label='作物生理', labeljust='l', fontsize='14', fontweight='bold',
                color='#3498db', style='filled', fillcolor='#fff')
        cc.node_attr.update(style='filled', fillcolor='#fff', color='#95a5a6')
        cc.node('dev_stage', '发育阶段计算')
        cc.node('photosynthesis', '光合作用')
        cc.node('respiration', '呼吸损耗')
        cc.node('dm_allocation', '干物质分配')
        cc.node('fruit_model', '果实群体建模')
        
        with cc.subgraph(name='cluster_stress') as cs:
            cs.attr(label='胁迫响应', labeljust='l', fontsize='12', fontweight='bold',
                    color='#e74c3c', style='filled', fillcolor='#fff5f5')
            cs.node_attr.update(style='filled', fillcolor='#fff', color='#e74c3c')
            cs.node('nutrient_stress', '养分胁迫')
            cs.node('water_stress', '水分胁迫')

with dot.subgraph(name='cluster_output') as c:
    c.attr(label='输出模块', labeljust='l', fontsize='16', fontweight='bold',
           color='#27ae60', style='filled', fillcolor='#e8f8e8')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#27ae60')
    c.node('quality', '品质指标')
    c.node('yield', '产量指标')
    c.node('biomass', '生物量指标')
    c.node('environment', '环境指标')

dot.node('formula_photo', 
         '光合作用:\nPG = PAR x RUE x f(T) x f(W) x f(N)\n温度响应:\nf(T) = piecewise函数(5C,20C,28C,35C)',
         shape='note', style='filled', fillcolor='#fff', color='#3498db', fontsize='10')

dot.node('formula_euler',
         '欧拉积分法:\nY(t+1) = Y(t) + dY/dt x dt\n每日更新状态量:\n- 生物量\n- 叶面积指数\n- 土壤含水量\n- 生理年龄',
         shape='note', style='filled', fillcolor='#fff', color='#3498db', fontsize='10')

dot.node('formula_fruit',
         '果实群体模型:\n1. 群体形成: N_cohort = f(开花率)\n2. 生理年龄: PA(t+1) = PA(t) + R_age\n3. 成熟条件: PA >= PA_thresh\n4. 产量计算: S(果实数 x 单果重)',
         shape='note', style='filled', fillcolor='#fff', color='#9b59b6', fontsize='10')

dot.edge('species', 'daily_loop', label='物候参数')
dot.edge('variety', 'daily_loop', label='光合参数')
dot.edge('weather', 'daily_loop', label='温度/辐射/降水')
dot.edge('management', 'daily_loop', label='灌溉/施肥')
dot.edge('soil', 'daily_loop', label='土壤参数')

dot.edge('daily_loop', 'met_process', label='气象数据')
dot.edge('met_process', 'swd_dynamic', label='蒸发需求')

dot.edge('daily_loop', 'dev_stage', label='热时间/GDD')
dot.edge('daily_loop', 'photosynthesis', label='PAR/温度')

dot.edge('swd_dynamic', 'nutrient_stress', label='土壤氮含量')
dot.edge('swd_dynamic', 'water_stress', label='土壤含水量')

dot.edge('dev_stage', 'photosynthesis', label='发育阶段')
dot.edge('dev_stage', 'respiration', label='发育阶段')
dot.edge('dev_stage', 'dm_allocation', label='发育阶段')
dot.edge('dev_stage', 'fruit_model', label='发育阶段')

dot.edge('nutrient_stress', 'photosynthesis', label='NSF_photo')
dot.edge('water_stress', 'photosynthesis', label='WSF_photo')

dot.edge('photosynthesis', 'respiration', label='总光合产物')
dot.edge('respiration', 'dm_allocation', label='净光合产物')
dot.edge('dm_allocation', 'fruit_model', label='分配至果实')

dot.edge('dm_allocation', 'photosynthesis', label='LAI反馈', color='#e74c3c', penwidth='2')

dot.edge('fruit_model', 'quality', label='SSC/TA')
dot.edge('fruit_model', 'yield', label='产量分布')
dot.edge('fruit_model', 'biomass', label='器官生物量')
dot.edge('swd_dynamic', 'environment', label='水氮动态')

output_dir = r'C:\Users\R9000P\Desktop\各种文件\CN-strawberryDSSAT-main\模型图片'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, '草莓模型原理图')

dot.render(output_file, view=True, cleanup=True)

print(f"原理图已保存到: {output_file}.png")
print(f"已打开图片")