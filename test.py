from resource.object_module import PostgresDatabase
from resource.object_module import MinioOss
from resource.task import SaveTask


def main():
    print(">>> 正在初始化模块...")

    # 实例化 Database
    try:
        db = PostgresDatabase()
        print("✅ Database 模块初始化成功")
    except Exception as e:
        print(f"❌ Database 初始化失败: {e}")
        return

    # 实例化 OSS
    try:
        oss = MinioOss()
        print("✅ OSS 模块初始化成功")
    except Exception as e:
        print(f"❌ OSS 初始化失败: {e}")
        return

    # 实例化 Task
    # 注意：task_id 随便给一个，type 随便给一个
    task = SaveTask(oss=oss, db=db, type="manual_test", task_id="test-001")

    print(">>> 开始执行任务...")

    # 运行
    task.run()

    # 结果检查
    if task.state == "SUCCESS":
        print("\n🎉🎉🎉 测试通过！备份任务执行成功！")
        print(f"请检查本地 logs/ 目录下的日志文件")
        print(f"请检查 MinIO Console 看 bucket 里有没有文件")
    else:
        print("\n💀💀💀 测试失败，请检查日志。")


if __name__ == "__main__":
    main()