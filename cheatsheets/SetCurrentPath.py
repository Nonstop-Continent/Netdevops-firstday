from pathlib import Path

# .resolve() 可以获取更规范的绝对路径（处理 '..' 和符号链接）
script_dir = Path(__file__).parent.resolve()
print(f"脚本所在目录 (绝对路径): {script_dir}")

# 获取父目录
parent_dir = script_dir.parent
print(f"脚本所在目录的父目录 (绝对路径): {parent_dir}")

# 如果文件就在脚本旁边
sibling_file_path = script_dir / '文件.xlsx'
print(f"同级文件路径: {sibling_file_path}")

# 检查文件是否存在
if sibling_file_path.is_file():
    print("文件存在")
    # 读取 Excel 文件 (示例)
    # df = pd.read_excel(inventory_path)
    # print(df.head())
    pass # 在这里添加实际的文件读取逻辑
else:
    print(f"错误：在路径 {sibling_file_path} 未找到文件。")