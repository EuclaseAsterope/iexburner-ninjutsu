import asyncio
import os
from lrz import NinjutsuPlugin  # 替换为你的插件模块名

#测试用例脚本
class MockEvent:
    def __init__(self, message):
        self.message_str = message
        self.sender_nickname = "测试用户"

    async def plain_result(self, text):
        print(f"[文本回复] {text}")
        return None

    async def chain_result(self, messages):
        for msg in messages:
            if hasattr(msg, "file"):  # 检测音频消息
                # 获取当前脚本所在目录
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # 设置新的输出路径和文件名
                new_path = os.path.join(script_dir, "ninjutsu.wav")

                # 重命名并移动文件到脚本目录
                try:
                    if os.path.exists(msg.file):
                        # 如果目标文件已存在则删除
                        if os.path.exists(new_path):
                            os.remove(new_path)
                        # 重命名文件
                        os.rename(msg.file, new_path)
                        print(f"[生成音频] 已保存到: {new_path}")
                    else:
                        print(f"[错误] 音频文件不存在: {msg.file}")
                except Exception as e:
                    print(f"[错误] 文件操作失败: {str(e)}")
        return None


async def run_plugin_command(plugin, command):
    """执行插件命令并处理所有响应"""
    event = MockEvent(command)
    async for response in plugin.cmd_ninjutsu(event):
        if asyncio.iscoroutine(response):
            await response


async def test():
    # 初始化插件
    plugin = NinjutsuPlugin(None)
    plugin.plugin_dir = os.path.dirname(os.path.abspath(__file__))  # 使用脚本所在目录
    plugin.sources_dir = os.path.join(plugin.plugin_dir, "sources")

    # 确保测试音频文件存在
    test_audio = "aiyin_soyo.wav"  # 改为测试用的音频文件名
    if not os.path.exists(plugin.sources_dir):
        os.makedirs(plugin.sources_dir)
    if not os.path.exists(os.path.join(plugin.sources_dir, test_audio)):
        with open(os.path.join(plugin.sources_dir, test_audio), 'wb') as f:
            f.write(
                b'RIFF\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00')

    # 测试1: 列出所有忍术
    print("\n=== 测试1: 列出所有忍术 ===")
    await run_plugin_command(plugin, "/释放忍术")

    # 测试2: 释放有效忍术
    print("\n=== 测试2: 释放有效忍术 ===")
    await run_plugin_command(plugin, "/释放忍术 1313112")

    # 测试3: 释放无效忍术
    print("\n=== 测试3: 释放无效忍术 ===")
    await run_plugin_command(plugin, "/释放忍术 未知忍术")



if __name__ == "__main__":
    asyncio.run(test())