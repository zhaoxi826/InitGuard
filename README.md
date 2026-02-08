**InitGuard**:基于postgres和redis的自动化数据库备份系统。

版本:v0.1  
功能：最基础的备份脚本

版本:v0,2
功能：可以通过web接口手动创建资源和任务，并自动化完成的备份程序，采用fastapi和SQLModel技术栈，对接外部的Postgres进行数据持久化与Redis进行任务队列和信息缓存。