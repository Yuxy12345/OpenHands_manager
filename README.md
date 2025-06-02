# OpenHands Manager

## 项目介绍
OpenHands Manager 是一个用于管理和监控OpenHands容器资源的系统。

OpenHands是由All-Hands-AI团队开发的开源AI软件开发代理平台：
https://github.com/All-Hands-AI/OpenHands

由于OpenHands当前只有单用户，故通过管理多容器的方式实现多用户使用。

## 整体架构
系统主要由以下几个模块构成：
- 前端：使用Vue框架构建用户界面，配合Vite作为构建工具。
- 后端：使用Flask框架构建服务端API，配合Flask-JWT-Extended实现身份验证。
- 数据库：使用SQLite作为默认数据库，存储用户信息和容器数据。
- 容器管理：使用Docker Python SDK动态创建和管理用户容器。
- 容器镜像：基于OpenHands镜像（docker.all-hands.dev/all-hands-ai/openhands:latest）创建容器。

## 运行方法
1. **环境准备**  
   - Python 3.8+
   - Node.js 14+
   - Docker Engine
   - SQLite（默认数据库）

    由于OpenHands需要在Linux/WSL上运行，故该项目也要在Linux/WSL上运行才能拉起可用的OpenHands容器。

2. **项目克隆**  
   ```bash
   git clone https://github.com/Yuxy12345/OpenHands_manager.git
   cd OpenHands_manager
   ```

3. **依赖安装**  
   - 安装前端依赖：
     ```bash
     cd frontend
     npm install
     ```
   - 安装后端依赖：
     ```bash
     cd backend
     pip install -r requirements.txt
     ```

4. **配置Docker环境**  
   - 确保Docker已安装并运行。
   - 确保可以访问Docker镜像仓库。

5. **启动项目**  
   
   - 运行后端服务：
     ```bash
     cd backend/src
     flask run --port=5000
     ```
   - 运行前端开发服务器：
     ```bash
     cd frontend
     npm run dev
     ```

6. **项目访问**  
   启动后，通过访问 `http://localhost:3000`（或根据配置的端口）使用系统。

## 许可证
   该项目使用Apache License授权。请参阅LICENSE文件以获取更多信息。

## 其他信息
   如果你在使用过程中遇到问题，请通过GitHub Issues提交问题。
   如果你有任何建议或想法，欢迎通过Pull Request贡献代码。
