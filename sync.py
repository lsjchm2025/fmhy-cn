import os

# ================= 配置区 =================
# 映射关键字: [中文展示名称, 你的自定义文件]
# 只要原文件名包含关键字（忽略大小写），就能匹配上
MAPPING = {
    "video": ["🎬 影视资源", "custom_video.txt"],
    "reading": ["📚 图书文献", "custom_books.txt"],
    "storage": ["☁️ 网盘工具", "custom_cloud.txt"],
    "download": ["📥 下载工具", "custom_tools.txt"],
    "gaming": ["🎮 游戏资源", "custom_games.txt"],
    "adblock": ["🛡️ 广告拦截", "custom_adblock.txt"],
    "non-english": ["🌐 全球资源", None]
}

UPSTREAM_DIR = "upstream"
SIDEBAR_FILE = "_sidebar.md"
# ==========================================

def get_custom_content(config_file):
    if config_file and os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return f"\n> [!TIP]\n> ### 🇨🇳 中文特供精选\n{content}\n\n---\n\n"
    return ""

def process_all():
    sidebar_items = ["* [🏠 首页](README.md)"]
    
    if not os.path.exists(UPSTREAM_DIR):
        print("❌ 错误: upstream 目录不存在！")
        return

    # 获取上游目录下所有的文件
    upstream_files = os.listdir(UPSTREAM_DIR)
    print(f"📂 正在扫描上游文件: {upstream_files}")

    # 遍历我们的映射配置
    for key, info in MAPPING.items():
        title_cn, custom_file = info
        target_file = None
        
        # 在上游文件中寻找包含关键字的文件（如寻找包含 'video' 的 .md 文件）
        for f in upstream_files:
            if key.lower() in f.lower() and f.endswith(".md"):
                target_file = f
                break
        
        if target_file:
            print(f"✅ 匹配成功: {key} -> {target_file}")
            src_path = os.path.join(UPSTREAM_DIR, target_file)
            
            with open(src_path, "r", encoding="utf-8") as f:
                original_lines = f.readlines()

            final_content = [f"# {title_cn}\n\n", get_custom_content(custom_file), "## 🌍 全球资源 (同步自 FMHY)\n\n"]
            
            for line in original_lines:
                if line.startswith("# "): continue
                final_content.append(line)

            # 统一输出文件名，方便 Docsify 访问
            output_name = f"{key.capitalize()}.md"
            with open(output_name, "w", encoding="utf-8") as f:
                f.writelines(final_content)
            
            sidebar_items.append(f"* [{title_cn}]({output_name})")
        else:
            print(f"❌ 未能匹配到关键字: {key}")

    # 强制写入侧边栏
    with open(SIDEBAR_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sidebar_items))
    print(f"✨ 侧边栏已更新，共 {len(sidebar_items)-1} 个条目")

if __name__ == "__main__":
    process_all()
