import os

graphviz_path = r'C:\Program Files\Graphviz\bin'
os.environ['PATH'] = graphviz_path + os.pathsep + os.environ.get('PATH', '')

import graphviz

dot = graphviz.Digraph('项目整体工作流程图', comment='CROPGRO-Strawberry项目整体工作流程图', format='png')

dot.attr(rankdir='TB', size='28,22', dpi='300', fontname='Microsoft YaHei', fontsize='12')
dot.node_attr.update(shape='box', style='rounded,filled', fontname='Microsoft YaHei', fontsize='11')
dot.edge_attr.update(fontname='Microsoft YaHei', fontsize='9')

with dot.subgraph(name='cluster_dataclass') as c:
    c.attr(label='数据类', labeljust='l', fontsize='14', fontweight='bold',
           color='#3498db', style='filled', fillcolor='#e8f4f8')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#3498db')
    c.node('PlantState', 'PlantState\n(植物状态)')

with dot.subgraph(name='cluster_njit') as c:
    c.attr(label='Numba优化函数', labeljust='l', fontsize='14', fontweight='bold',
           color='#f39c12', style='filled', fillcolor='#fff8e7')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#f39c12')
    c.node('_calc_daylength', '_calc_daylength()\n计算日长')
    c.node('_thermal_time', '_thermal_time()\n计算热时间')
    c.node('_photosynthesis', '_photosynthesis()\n光合作用')
    c.node('_transpiration', '_transpiration()\n蒸腾作用')
    c.node('_water_stress', '_water_stress()\n水分胁迫')
    c.node('_maintenance_resp', '_maintenance_resp()\n维持呼吸')

with dot.subgraph(name='cluster_class') as c:
    c.attr(label='CropgroStrawberry类', labeljust='l', fontsize='14', fontweight='bold',
           color='#27ae60', style='filled', fillcolor='#e8f8e8')
    c.node_attr.update(style='filled', fillcolor='#fff', color='#27ae60')
    
    with c.subgraph(name='cluster_init') as ci:
        ci.attr(label='初始化', labeljust='l', fontsize='12', fontweight='bold',
                color='#2ecc71', style='filled', fillcolor='#f0fff4')
        ci.node_attr.update(style='filled', fillcolor='#fff', color='#2ecc71')
        ci.node('__init__', '__init__()\n初始化模型')
    
    with c.subgraph(name='cluster_phenology') as cp:
        cp.attr(label='物候发育', labeljust='l', fontsize='12', fontweight='bold',
                color='#3498db', style='filled', fillcolor='#f0f8ff')
        cp.node_attr.update(style='filled', fillcolor='#fff', color='#3498db')
        cp.node('calculate_daylength', 'calculate_daylength()')
        cp.node('calculate_thermal_time', 'calculate_thermal_time()')
        cp.node('update_phenology', 'update_phenology()')
    
    with c.subgraph(name='cluster_physiology') as cph:
        cph.attr(label='生理过程', labeljust='l', fontsize='12', fontweight='bold',
                 color='#9b59b6', style='filled', fillcolor='#faf5ff')
        cph.node_attr.update(style='filled', fillcolor='#fff', color='#9b59b6')
        cph.node('calculate_photosynthesis', 'calculate_photosynthesis()')
        cph.node('calculate_transpiration', 'calculate_transpiration()')
        cph.node('calculate_water_stress', 'calculate_water_stress()')
        cph.node('calculate_maintenance_resp', 'calculate_maintenance_resp()')
        cph.node('partition_biomass', 'partition_biomass()')
    
    with c.subgraph(name='cluster_reproductive') as cr:
        cr.attr(label='繁殖更新', labeljust='l', fontsize='12', fontweight='bold',
                color='#e74c3c', style='filled', fillcolor='#fff5f5')
        cr.node_attr.update(style='filled', fillcolor='#fff', color='#e74c3c')
        cr.node('update_runners', 'update_runners()')
        cr.node('update_crowns', 'update_crowns()')
        cr.node('update_fruits', 'update_fruits()')
    
    with c.subgraph(name='cluster_simulation') as cs:
        cs.attr(label='模拟控制', labeljust='l', fontsize='12', fontweight='bold',
                color='#2c3e50', style='filled', fillcolor='#f0f3f4')
        cs.node_attr.update(style='filled', fillcolor='#fff', color='#2c3e50')
        cs.node('simulate_day', 'simulate_day()')
        cs.node('simulate_growth', 'simulate_growth()')
        cs.node('plot_results', 'plot_results()')

dot.edge('__init__', 'PlantState', label='初始化')

dot.edge('calculate_daylength', '_calc_daylength', label='调用')
dot.edge('calculate_thermal_time', '_thermal_time', label='调用')
dot.edge('calculate_photosynthesis', '_photosynthesis', label='调用')
dot.edge('calculate_transpiration', '_transpiration', label='调用')
dot.edge('calculate_water_stress', '_water_stress', label='调用')
dot.edge('calculate_maintenance_resp', '_maintenance_resp', label='调用')

dot.edge('simulate_growth', 'simulate_day', label='循环调用')

dot.edge('simulate_day', 'calculate_daylength', label='计算日长')
dot.edge('simulate_day', 'calculate_thermal_time', label='计算热时间')
dot.edge('simulate_day', 'update_phenology', label='更新物候')
dot.edge('simulate_day', 'calculate_photosynthesis', label='计算光合')
dot.edge('simulate_day', 'calculate_transpiration', label='计算蒸腾')
dot.edge('simulate_day', 'calculate_water_stress', label='计算水分胁迫')
dot.edge('simulate_day', 'calculate_maintenance_resp', label='计算呼吸')
dot.edge('simulate_day', 'partition_biomass', label='分配生物量')
dot.edge('simulate_day', 'update_runners', label='更新匍匐茎')
dot.edge('simulate_day', 'update_crowns', label='更新冠数')
dot.edge('simulate_day', 'update_fruits', label='更新果实')

dot.edge('partition_biomass', 'PlantState', label='更新状态')
dot.edge('update_runners', 'PlantState', label='更新状态')
dot.edge('update_crowns', 'PlantState', label='更新状态')
dot.edge('update_fruits', 'PlantState', label='更新状态')

dot.edge('simulate_growth', 'plot_results', label='输出结果')
dot.edge('plot_results', 'PlantState', label='读取状态')

dot.edge('simulate_day', 'PlantState', label='读取/写入')

output_dir = r'C:\Users\R9000P\Desktop\各种文件\CN-strawberryDSSAT-main\模型图片'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, '项目整体工作流程图')

dot.render(output_file, view=True, cleanup=True)

print(f"项目整体工作流程图已保存到: {output_file}.png")
print(f"已打开图片")