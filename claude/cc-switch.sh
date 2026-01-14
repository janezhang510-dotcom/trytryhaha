#!/bin/bash

# 显示当前模型信息
echo "当前 Claude Code CLI 版本: $(claude --version 2>/dev/null || echo "未安装")"
echo "默认模型: Auto (系统会自动选择)"
echo ""

# 显示模型选项
echo "可用模型选项:"
echo "1. Auto (自动选择)"
echo "2. Sonnet (claude-sonnet)"
echo "3. Opus (claude-opus)"
echo "4. Gemini (Google Gemini)"
echo ""

# 提示用户选择
read -p "请输入模型编号 (1-4): " choice

# 根据选择执行相应命令
case $choice in
    1)
        echo "已选择 Auto 模型，直接运行 'claude' 即可启动"
        ;;
    2)
        echo "已选择 Sonnet 模型，运行以下命令启动:"
        echo "claude --model sonnet"
        ;;
    3)
        echo "已选择 Opus 模型，运行以下命令启动:"
        echo "claude --model opus"
        ;;
    4)
        echo "已选择 Gemini 模型，正在配置..."
        echo ""
        
        # 检查是否已配置 Gemini MCP 服务器
        if ! claude mcp list | grep -q "gemini"; then
            echo "正在添加 Gemini MCP 服务器..."
            
            # 提示用户输入 Gemini API 密钥
            read -p "请输入 Google Gemini API 密钥: " gemini_api_key
            
            if [ -z "$gemini_api_key" ]; then
                echo "错误: API 密钥不能为空"
                exit 1
            fi
            
            # 创建 Gemini MCP 配置
            gemini_config='{
                "name": "gemini",
                "transport": "stdio",
                "command": "bash",
                "args": [
                    "-c",
                    "npm install -g gemini-mcp-server && GEMINI_API_KEY='$gemini_api_key' gemini-mcp-server"
                ]
            }'
            
            # 添加 MCP 服务器
            echo "$gemini_config" > gemini-mcp-config.json
            claude mcp add-from-claude-desktop || echo "自动配置失败，请手动配置"
            
            echo "Gemini MCP 服务器配置完成"
        else
            echo "Gemini MCP 服务器已配置"
        fi
        
        echo ""
        echo "运行以下命令启动 Gemini 模型:"
        echo "claude --model gemini"
        ;;
    *)
        echo "无效选择，请重新运行脚本"
        exit 1
        ;;
esac