# b_task.py
import argparse
import logging
import os
import socket
import json
import sys, io
import time

from main import ask
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('testb.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
logger.info("当前工作目录: %s", os.getcwd())

def run_task():
    """模拟执行任务"""
    print("子程序B：任务开始...")
    time.sleep(1)  # 模拟耗时操作
    result = {
        "status": "success",
        "data": [1, 2, 3, 4, 5],
        "message": "任务执行完成",
        "timestamp": time.time()
    }
    return result


def send_result_to_a(data, host, port):
    json_data = json.dumps(data).encode('utf-8')
    for i in range(3):  # 最多重试3次
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(json_data)
                print(f"子程序B：结果已发送到 {host}:{port}")
                return
        except ConnectionRefusedError:
            print(f"子程序B：连接被拒绝，重试 {i + 1}/3...")
            time.sleep(0.5)
    print("❌ 子程序B：无法连接到主程序A，请确保A已在监听")


if __name__ == "__main__":
    # 从命令行参数获取 A 的 socket 地址
    if len(sys.argv) != 3:
        print("用法: python b_task.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    parser = argparse.ArgumentParser(description="Run the Deer")
    parser.add_argument("query", nargs="*", help="The query to process")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode with built-in questions",
    )
    parser.add_argument(
        "--max_plan_iterations",
        type=int,
        default=1,
        help="Maximum number of plan iterations (default: 1)",
    )
    parser.add_argument(
        "--max_step_num",
        type=int,
        default=3,
        help="Maximum number of steps in a plan (default: 3)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--no-background-investigation",
        action="store_false",
        dest="enable_background_investigation",
        help="Disable background investigation before planning",
    )

    args = parser.parse_args()

    # todo, mock
    with open(r'C:\coding\project\deer-flow\download_commands.txt', 'r', encoding='utf-8') as f:
        mock_query = f.read()
    args.query = mock_query

    user_query = args.query
    # Run the agent workflow with the provided parameters
    final_result_dict: dict = {}
    print("Python 执行路径:", sys.executable)
    ask(
        question=user_query,
        debug=args.debug,
        max_plan_iterations=args.max_plan_iterations,
        max_step_num=args.max_step_num,
        enable_background_investigation=args.enable_background_investigation,
        final_result_dict=final_result_dict,
    )
    logger.info("b-get-end")
    # 发送结果
    send_result_to_a(final_result_dict['result'], host, port)
    logger.info("b-end")
