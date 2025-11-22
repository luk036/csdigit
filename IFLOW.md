# CSDigit iFlow Context

## 项目概述

CSDigit 是一个 Python 库，用于在十进制数和规范符号数字 (Canonical Signed Digit, CSD) 表示之间进行转换。CSD 是一种特殊的符号数字表示法，其中每个数字被限制为 -1、0 或 1，且不允许连续的非零数字。这种表示法在数字信号处理应用中特别有用，例如滤波器设计，因为它能通过使用简单的加法器和减法器来实现高效算术运算。

## 主要功能

- `to_csd`: 将十进制数转换为 CSD 字符串
- `to_csd_i`: 将整数转换为 CSD 字符串
- `to_decimal`: 将 CSD 字符串转换为十进制数
- `to_csdnnz`: 具有最大非零位数限制的 CSD 转换
- `to_csdnnz_i`: 整数版本的 CSD 转换，带非零位数限制
- `longest_repeated_substring`: 查找 CSD 字符串中的最长重复子串
- `generate_csd_multiplier`: 生成 CSD 乘法器的 Verilog 代码

## 项目结构

- `src/csdigit/`: 源代码目录
  - `csd.py`: 核心 CSD 转换函数
  - `cli.py`: 命令行接口
  - `csd_multiplier.py`: CSD 乘法器 Verilog 代码生成
  - `lcsre.py`: 最长重复子串查找算法
- `tests/`: 测试代码
- `docs/`: 文档
- `requirements/`: 依赖配置

## 构建和运行

### 安装依赖
```bash
pip install -r requirements.txt
```

### 开发安装
```bash
pip install -e .
```

### 运行测试
```bash
pytest tests/
```

### 使用命令行工具
```bash
# 转换十进制到 CSD
python -m csdigit.cli -c 28.5 -p 2

# 转换 CSD 到十进制
python -m csdigit.cli -d "+00-00.+"

# 使用非零位数限制
python -m csdigit.cli -f 28.5 -z 4
```

## 开发约定

- 遵循 Python PEP 8 代码风格
- 使用 pytest 进行测试
- 使用 doctest 进行函数示例测试
- 使用 type hints 提供类型信息
- 遵循语义化版本控制

## 测试

项目包含全面的单元测试，使用 pytest 和 hypothesis 进行属性测试。主要测试包括:
- CSD 转换的正确性
- 反向转换验证 (decimal -> CSD -> decimal)
- 特殊情况处理 (零值、负数)
- 边界条件测试

## 许可证

MIT 许可证