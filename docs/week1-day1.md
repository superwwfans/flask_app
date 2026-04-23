# Week1 Day1 - Baseline Execution & Diagnostics

## 1) 执行命令
在仓库根目录 `/workspace/flask_app` 执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt 2>&1 | tee day1_pip_install.log

export DB_URI='mysql+pymysql://user:pass@127.0.0.1:3306/blog'
export MAIL_SERVER='smtp.example.com'
export MAIL_USERNAME='noreply@example.com'
export MAIL_PASSWORD='replace_me'
export ADMINS='admin@example.com'

timeout 30s python app.py 2>&1 | tee day1_app_start.log || true
rg -n "Traceback|ERROR|Exception|ModuleNotFoundError|ImportError|OperationalError" day1_pip_install.log day1_app_start.log || true
```

## 2) 结果状态
- 状态：**配置 + 依赖阻塞**（尚不可启动）
- 说明：`pip` 无法从包源获取依赖，导致 Flask 未安装，应用无法启动。

## 3) 错误摘要
- 依赖安装日志（`day1_pip_install.log`）中出现：
  - `ERROR: Could not find a version that satisfies the requirement alembic==0.9.5`
  - `ERROR: No matching distribution found for alembic==0.9.5`
- 启动日志（`day1_app_start.log`）中出现：
  - `ModuleNotFoundError: No module named 'flask'`

## 4) 下一步建议（Day2 输入）
1. 优先修复构建网络：
   - 检查 CI/容器代理配置（当前返回 `Tunnel connection failed: 403 Forbidden`）。
   - 切换到可访问镜像源后重新安装 `requirements.txt`。
2. 依赖可安装后，重新执行 Day1 启动命令，确认 Flask App 可拉起。
3. 若启动后出现 DB 连接失败，再区分为外部依赖阻塞（MySQL/Redis）并补充最小连通性验证。
