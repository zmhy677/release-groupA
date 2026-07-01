import os

graphviz_path = r'C:\Program Files\Graphviz\bin'
os.environ['PATH'] = graphviz_path + os.pathsep + os.environ.get('PATH', '')

import graphviz

dot = graphviz.Digraph('代码函数关系图', comment='CROPGRO-Strawberry代码函数与类结构关系图', format='png')

dot.attr(rankdir='TB', size='40,36', dpi='300', fontname='Microsoft YaHei', fontsize='14', nodesep='1.8', ranksep='2.2')
dot.node_attr.update(shape='box', style='rounded,filled', fontname='Microsoft YaHei', fontsize='14', width='3.5', height='1.2')
dot.edge_attr.update(fontname='Microsoft YaHei', fontsize='11', dir='forward', penwidth='2')

with dot.subgraph(name='cluster_input') as c:
    c.attr(label='输入数据', labeljust='l', fontsize='16', fontweight='bold',
           color='#3498db', style='filled', fillcolor='#e8f4f8')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#3498db')
    with c.subgraph(name='rank_input') as ri:
        ri.attr(rank='same')
        c.node('solar', '太阳辐射')
        c.node('temp', '温度')
        c.node('rainfall', '降雨量')
        c.node('rh', '相对湿度')
        c.node('wind', '风速')

dot.node('simulate_growth', 'simulate_growth()\n模拟生长', style='filled', fillcolor='#2c3e50', fontcolor='white', fontsize='16')

dot.node('simulate_day', 'simulate_day()\n每日模拟', style='filled', fillcolor='#2980b9', fontcolor='white', fontsize='16')

with dot.subgraph(name='cluster_flow') as c:
    c.attr(label='计算流程', labeljust='l', fontsize='16', fontweight='bold',
           color='#f39c12', style='filled', fillcolor='#fff8e7')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#f39c12')
    
    c.node('step1', '1. 日长计算')
    c.node('step2', '2. 热时间计算')
    c.node('step3', '3. 物候更新')
    c.node('step4', '4. 光合作用')
    c.node('step5', '5. 蒸腾作用')
    c.node('step6', '6. 水分胁迫')
    c.node('step7', '7. 维持呼吸')
    c.node('step8', '8. 生物量分配')
    c.node('step9', '9. 繁殖更新')

with dot.subgraph(name='cluster_njit') as c:
    c.attr(label='底层函数', labeljust='l', fontsize='16', fontweight='bold',
           color='#9b59b6', style='filled', fillcolor='#faf5ff')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#9b59b6')
    with c.subgraph(name='rank_njit') as rn:
        rn.attr(rank='same')
        c.node('njit1', '_calc_daylength()')
        c.node('njit2', '_thermal_time()')
        c.node('njit3', '_photosynthesis()')
        c.node('njit4', '_transpiration()')
        c.node('njit5', '_water_stress()')
        c.node('njit6', '_maintenance_resp()')

with dot.subgraph(name='cluster_state') as c:
    c.attr(label='状态变量', labeljust='l', fontsize='16', fontweight='bold',
           color='#27ae60', style='filled', fillcolor='#e8f8e8')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#27ae60')
    
    with c.subgraph(name='rank_state1') as rs:
        rs.attr(rank='same')
        c.node('st_bio', '总生物量')
        c.node('st_lai', '叶面积指数')
        c.node('st_depth', '根系深度')
    
    with c.subgraph(name='rank_state2') as rs:
        rs.attr(rank='same')
        c.node('st_fruit', '果实生物量')
        c.node('st_stage', '物候阶段')
        c.node('st_crown', '冠数')
        c.node('st_runner', '匍匐茎数')

dot.node('plot', 'plot_results()\n结果输出', style='filled', fillcolor='#e74c3c', fontcolor='white', fontsize='16')

dot.edge('solar', 'simulate_day', label='')
dot.edge('temp', 'simulate_day', label='')
dot.edge('rainfall', 'simulate_day', label='')
dot.edge('rh', 'simulate_day', label='')
dot.edge('wind', 'simulate_day', label='')

dot.edge('simulate_growth', 'simulate_day', label='循环')

dot.edge('simulate_day', 'step1', label='')
dot.edge('step1', 'step2', label='')
dot.edge('step2', 'step3', label='')
dot.edge('step3', 'step4', label='')
dot.edge('step4', 'step5', label='')
dot.edge('step5', 'step6', label='')
dot.edge('step6', 'step7', label='')
dot.edge('step7', 'step8', label='')
dot.edge('step8', 'step9', label='')

dot.edge('step1', 'njit1', label='调用', constraint='false')
dot.edge('step2', 'njit2', label='调用', constraint='false')
dot.edge('step4', 'njit3', label='调用', constraint='false')
dot.edge('step5', 'njit4', label='调用', constraint='false')
dot.edge('step6', 'njit5', label='调用', constraint='false')
dot.edge('step7', 'njit6', label='调用', constraint='false')

dot.edge('step3', 'st_stage', label='更新', constraint='false')
dot.edge('step8', 'st_bio', label='更新', constraint='false')
dot.edge('step8', 'st_lai', label='更新', constraint='false')
dot.edge('step8', 'st_depth', label='更新', constraint='false')
dot.edge('step8', 'st_fruit', label='更新', constraint='false')
dot.edge('step9', 'st_crown', label='更新', constraint='false')
dot.edge('step9', 'st_runner', label='更新', constraint='false')

dot.edge('step4', 'st_lai', label='读取', constraint='false')
dot.edge('step6', 'st_depth', label='读取', constraint='false')

dot.edge('simulate_growth', 'plot', label='输出')
dot.edge('plot', 'st_bio', label='读取', constraint='false')
dot.edge('plot', 'st_lai', label='读取', constraint='false')

output_dir = r'C:\Users\R9000P\Desktop\各种文件\CN-strawberryDSSAT-main\模型图片'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, '代码函数关系图')

dot.render(output_file, view=True, cleanup=True)

print(f"代码函数关系图已保存到: {output_file}.png")
print(f"已打开图片")