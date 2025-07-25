from openai import OpenAI
import time  # 导入时间模块
import pyperclip  # 用于操作剪贴板

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

def get_command(chinese_description):
    prompt = f"将下面的中文描述转换为对应的命令行指令，只返回命令本身，不做额外解释：\n{chinese_description}"
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        },
        model="moonshotai/kimi-k2:free",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("中文转命令行工具（输入'退出'或'q'结束程序）")
    print("=" * 40)
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n请输入中文命令描述：")
            
            # 检查退出条件
            if user_input.lower() in ['退出', 'q', 'quit', 'exit']:
                print("\n程序已退出，再见！")
                time.sleep(3)  # 等待3秒后再退出（可根据需要调整秒数）
                break
            
            # 生成并显示命令
            if user_input.strip():  # 忽略空输入
                command = get_command(user_input)
                print(f"对应的命令：{command}")
                # 尝试复制到剪贴板
                try:
                    pyperclip.copy(command)
                    # 验证复制是否成功
                    if pyperclip.paste() == command:
                        print("✅ 命令已复制到剪贴板，可直接粘贴使用")
                    else:
                        print("⚠️ 命令复制失败，请手动复制")
                except pyperclip.PyperclipException:
                    print("⚠️ 剪贴板操作失败，请手动复制")
            else:
                print("请输入有效的描述内容")
                
        except KeyboardInterrupt:
            # 处理Ctrl+C中断
            print("\n程序已退出，再见！")
            time.sleep(1)  # 等待3秒
            break
        except Exception as e:
            print(f"发生错误：{str(e)}，请重试")