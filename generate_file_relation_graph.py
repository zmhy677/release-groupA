import os

graphviz_path = r'C:\Program Files\Graphviz\bin'
os.environ['PATH'] = graphviz_path + os.pathsep + os.environ.get('PATH', '')

import graphviz

dot = graphviz.Digraph('文件关系图', comment='CROPGRO-Strawberry项目文件关系图', format='png')

dot.attr(rankdir='TB', size='36,28', dpi='300', fontname='Microsoft YaHei', fontsize='14', nodesep='1.0', ranksep='1.5')
dot.node_attr.update(fontname='Microsoft YaHei', fontsize='13')
dot.edge_attr.update(fontname='Microsoft YaHei', fontsize='10', dir='forward', penwidth='2')

with dot.subgraph(name='cluster_input_files') as c:
    c.attr(label='输入数据文件', labeljust='l', fontsize='16', fontweight='bold',
           color='#3498db', style='filled', fillcolor='#e8f4f8')
    c.node_attr.update(shape='folder', style='filled', fillcolor='#fff', color='#3498db')
    c.node('dir_strawberry', 'Strawberry/')
    c.node('dir_weather', 'Weather/')
    c.node('dir_soil', 'Soil/')

with dot.subgraph(name='cluster_srx_files') as c:
    c.attr(label='SRX实验文件', labeljust='l', fontsize='14', fontweight='bold',
           color='#2980b9', style='filled', fillcolor='#f0f8ff')
    c.node_attr.update(shape='note', style='filled', fillcolor='#fff', color='#2980b9')
    c.node('srx_1401', 'UFBA1401.SRX')
    c.node('srx_1601', 'UFBA1601.SRX')
    c.node('srx_1701', 'UFBA1701.SRX')
    c.node('srx_wm', 'UFWM1401.SRX')

with dot.subgraph(name='cluster_wth_files') as c:
    c.attr(label='WTH气象文件', labeljust='l', fontsize='14', fontweight='bold',
           color='#3498db', style='filled', fillcolor='#f0f8ff')
    c.node_attr.update(shape='note', style='filled', fillcolor='#fff', color='#3498db')
    c.node('wth_ba14', 'UFBA14.WTH')
    c.node('wth_ba16', 'UFBA16.WTH')
    c.node('wth_ba17', 'UFBA17.WTH')
    c.node('wth_wm14', 'UFWM14.WTH')

with dot.subgraph(name='cluster_soil_files') as c:
    c.attr(label='SOL土壤文件', labeljust='l', fontsize='14', fontweight='bold',
           color='#27ae60', style='filled', fillcolor='#e8f8e8')
    c.node_attr.update(shape='note', style='filled', fillcolor='#fff', color='#27ae60')
    c.node('sol_uf', 'UF.SOL')

with dot.subgraph(name='cluster_main_scripts') as c:
    c.attr(label='主脚本文件', labeljust='l', fontsize='16', fontweight='bold',
           color='#f39c12', style='filled', fillcolor='#fff8e7')
    c.node_attr.update(shape='box', style='rounded,filled', fillcolor='#fff', color='#f39c12')
    c.node('main_script', 'cropgro-strawberry-\nimplementation.py')
    c.node('test_script', 'cropgro-strawberry-\ntest1.py')
    c.node('validate_script', 'validate_models.py')
    c.node('run_dssat_script', 'run_original_dssat.py')

with dot.subgraph(name='cluster_output_files') as c:
    c.attr(label='输出文件', labeljust='l', fontsize='16', fontweight='bold',
           color='#e74c3c', style='filled', fillcolor='#fff5f5')
    c.node_attr.update(shape='folder', style='filled', fillcolor='#fff', color='#e74c3c')
    c.node('dir_test', '测试/')
    c.node('dir_model_images', '模型图片/')
    c.node('dir_comparison', 'comparison_reports/')

with dot.subgraph(name='cluster_output_png') as c:
    c.attr(label='图表文件', labeljust='l', fontsize='14', fontweight='bold',
           color='#e74c3c', style='filled', fillcolor='#fff0f0')
    c.node_attr.update(shape='note', style='filled', fillcolor='#fff', color='#e74c3c')
    c.node('png_1401', 'UFBA1401.png')
    c.node('png_compare', '年份对比图.png')
    c.node('png_biomass', 'UFBA1401_生物量变化.png')
    c.node('png_photo', 'UFBA1401_光合速率变化.png')
    c.node('png_lai', 'UFBA1401_叶面积指数变化.png')
    c.node('png_root', 'UFBA1401_根系深度变化.png')

with dot.subgraph(name='cluster_output_csv') as c:
    c.attr(label='数据文件', labeljust='l', fontsize='14', fontweight='bold',
           color='#9b59b6', style='filled', fillcolor='#faf5ff')
    c.node_attr.update(shape='note', style='filled', fillcolor='#fff', color='#9b59b6')
    c.node('csv_1401', 'UFBA1401.csv')
    c.node('csv_1601', 'UFBA1601.csv')
    c.node('csv_1701', 'UFBA1701.csv')
    c.node('csv_wm', 'UFWM1401.csv')

with dot.subgraph(name='cluster_diagram_png') as c:
    c.attr(label='图表文件', labeljust='l', fontsize='14', fontweight='bold',
           color='#2c3e50', style='filled', fillcolor='#f0f3f4')
    c.node_attr.update(shape='note', style='filled', fillcolor='#fff', color='#2c3e50')
    c.node('diagram_model', '草莓模型原理图.png')
    c.node('diagram_workflow', '项目整体工作流程图.png')
    c.node('diagram_function', '代码函数关系图.png')
    c.node('diagram_script', '程序脚本流程图.png')

dot.edge('dir_strawberry', 'srx_1401', label='')
dot.edge('dir_strawberry', 'srx_1601', label='')
dot.edge('dir_strawberry', 'srx_1701', label='')
dot.edge('dir_strawberry', 'srx_wm', label='')

dot.edge('dir_weather', 'wth_ba14', label='')
dot.edge('dir_weather', 'wth_ba16', label='')
dot.edge('dir_weather', 'wth_ba17', label='')
dot.edge('dir_weather', 'wth_wm14', label='')

dot.edge('dir_soil', 'sol_uf', label='')

dot.edge('srx_1401', 'main_script', label='解析')
dot.edge('srx_1601', 'main_script', label='解析')
dot.edge('srx_1701', 'main_script', label='解析')
dot.edge('srx_wm', 'main_script', label='解析')

dot.edge('wth_ba14', 'main_script', label='读取')
dot.edge('wth_ba16', 'main_script', label='读取')
dot.edge('wth_ba17', 'main_script', label='读取')
dot.edge('wth_wm14', 'main_script', label='读取')

dot.edge('sol_uf', 'main_script', label='读取')

dot.edge('main_script', 'test_script', label='依赖')
dot.edge('main_script', 'validate_script', label='依赖')

dot.edge('main_script', 'dir_test', label='输出')
dot.edge('main_script', 'dir_model_images', label='输出')

dot.edge('validate_script', 'dir_comparison', label='输出')

dot.edge('dir_test', 'png_1401', label='')
dot.edge('dir_test', 'png_compare', label='')
dot.edge('dir_test', 'png_biomass', label='')
dot.edge('dir_test', 'png_photo', label='')
dot.edge('dir_test', 'png_lai', label='')
dot.edge('dir_test', 'png_root', label='')

dot.edge('dir_test', 'csv_1401', label='')
dot.edge('dir_test', 'csv_1601', label='')
dot.edge('dir_test', 'csv_1701', label='')
dot.edge('dir_test', 'csv_wm', label='')

dot.edge('dir_model_images', 'diagram_model', label='')
dot.edge('dir_model_images', 'diagram_workflow', label='')
dot.edge('dir_model_images', 'diagram_function', label='')
dot.edge('dir_model_images', 'diagram_script', label='')

output_dir = r'C:\Users\R9000P\Desktop\各种文件\CN-strawberryDSSAT-main\模型图片'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, '文件关系图')

dot.render(output_file, view=True, cleanup=True)

print(f"文件关系图已保存到: {output_file}.png")
print(f"已打开图片")