import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.adapters.onebot.v11 import Adapter as OneBotAdapter
from nonebot.plugin import PluginMetadata
import pathlib
import base64
from nonebot_plugin_apscheduler import scheduler


pic_path = ["./congyu/congyu.jpg"]
picsend_group = ["123456"]


__plugin_meta__ = PluginMetadata(
    name="Image Sending Plugin",
    description="A plugin that sends images from specified paths to specified group chats and has a test function, also sends pictures automatically at 7 am and 8 pm.",
    usage="Use'send_pics' command to send pictures. Use 'test_send_pics' command to test if the picture sending works.",
    type="application",
    supported_adapters={"nonebot.adapters.onebot.v11"},
)


# 定义一个函数用于发送图片
async def send_images(bot: Bot):
    for pic in pic_path:
        pic_path_obj = pathlib.Path(pic)
        if pic_path_obj.exists():
            with open(pic_path_obj, "rb") as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                image = MessageSegment.image(f"data:image/jpeg;base64,{base64_image}")
                for group in picsend_group:
                    await bot.send_group_msg(group_id=int(group), message=image)
                    # 图片发送成功后发送消息
                    await bot.send_group_msg(group_id=int(group), message="Ciallo～(∠・ω< )⌒★ \n早上中午晚上好！我是吹丛雨bot~")
        else:
            nonebot.logger.warning(f"图片路径 {pic} 不存在，请检查配置。")


# 发送图片命令
send_pics_command = on_command("send_pics")


@send_pics_command.handle()
async def handle_send_pics_command(bot: Bot, event: Event):
    await send_images(bot)


# 测试图片发送命令
test_send_pics_command = on_command("test_send_picsLsl")


@test_send_pics_command.handle()
async def handle_test_send_pics_command(bot: Bot, event: Event):
    try:
        await send_images(bot)
        await test_send_pics_command.finish("图片发送测试成功！")
    except Exception as e:
        await test_send_pics_command.finish(f"图片发送测试失败，错误信息：{e}")


# 定时在早上7点发送图片的任务
@scheduler.scheduled_job('cron', hour=7, minute=21)
async def scheduled_send_images_morning():
    bot = nonebot.get_bot()
    await send_images(bot)


# 定时在晚上8点发送图片的任务
@scheduler.scheduled_job('cron', hour=19, minute=21)
async def scheduled_send_images_evening():
    bot = nonebot.get_bot()
    await send_images(bot)
