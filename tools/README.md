# 工具脚本

本目录包含项目相关的辅助工具脚本。

## 工具说明

- `organize_history.py` - 将历史markdown文件按年/月进行归类整理

## 使用方法

```bash
python tools/organize_history.py
```

该脚本会扫描markdowns目录下的所有历史文件，并按照文件名中的日期（YYYY-MM-DD格式）将它们移动到对应的年/月子目录中。