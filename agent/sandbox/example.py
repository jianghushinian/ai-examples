import asyncio
import base64
from playwright.async_api import async_playwright
from agent_sandbox import Sandbox


async def site_to_markdown():
    # 初始化沙盒客户端
    c = Sandbox(base_url="http://localhost:8080")
    home_dir = c.sandbox.get_context().home_dir

    # 浏览器：自动化下载 html
    async with async_playwright() as p:
        browser_info = c.browser.get_info().data
        page = await (await p.chromium.connect_over_cdp(browser_info.cdp_url)).new_page(
            viewport={
                "width": browser_info.viewport.width,
                "height": browser_info.viewport.height,
            }
        )
        await page.goto("https://sandbox.agent-infra.com/", wait_until="networkidle")
        html = await page.content()
        screenshot_b64 = base64.b64encode(
            await page.screenshot(full_page=False, type='png')
        ).decode('utf-8')

    # Jupyter：在沙盒中运行代码将 html 转换为 markdown
    c.jupyter.execute_code(
        code=f"""
from markdownify import markdownify
html = '''{html}'''
screenshot_b64 = "{screenshot_b64}"

md = f"{{markdownify(html)}}\\n\\n![Screenshot](data:image/png;base64,{{screenshot_b64}})"

with open('{home_dir}/site.md', 'w') as f:
    f.write(md)

print("完成！")
"""
    )

    # Bash：执行命令列出沙盒中的文件
    list_result = c.shell.exec_command(command=f"ls -lh {home_dir}")
    print(f"\n沙盒主目录中的文件：\n{list_result.data.output}")

    open("./output.md", "w").write(
        c.file.read_file(file=f"{home_dir}/site.md").data.content
    )

    return "./output.md"


if __name__ == "__main__":
    # 运行异步函数
    result = asyncio.run(site_to_markdown())
    print(f"\nMarkdown 文件保存在：{result}")