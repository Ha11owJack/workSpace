from aiogram.utils import executor

if __name__ == '__main__':
    from admin_panel import dp
    from other_panel import dp

    executor.start_polling(dp)
    # start_webhook(
    #      dispatcher=dp,
    #      webhook_path="/info.php/?num",
    #      on_startup=on_startup,
    #      on_shutdown=on_shutdown,
    #      skip_updates=True,
    #      host="10.20.13.124",
    #      port="80",
    # )
