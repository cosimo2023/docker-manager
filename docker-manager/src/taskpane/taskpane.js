Office.onReady((info) => {
    if (info.host === Office.HostType.Word) {
        document.getElementById("run").onclick = run;
    }
});

async function run() {
    try {
        console.log('开始处理文本');
        // 显示加载状态
        document.getElementById("loading").style.display = "block";
        document.getElementById("error").style.display = "none";
        
        await Word.run(async (context) => {
            const selection = context.document.getSelection();
            selection.load("text");
            await context.sync();

            if (!selection.text.trim()) {
                throw new Error("请先选择要优化的文本");
            }

            const selectedText = selection.text;
            console.log('选中的文本:', selectedText);
            
            const optimizedText = await optimizeText(selectedText);
            console.log('优化后的文本:', optimizedText);

            selection.insertText(optimizedText, Word.InsertLocation.replace);
            await context.sync();
        });
    } catch (error) {
        console.error('发生错误:', error);
        document.getElementById("error").textContent = `错误：${error.message}`;
        document.getElementById("error").style.display = "block";
    } finally {
        document.getElementById("loading").style.display = "none";
    }
}

async function optimizeText(text) {
    try {
        const response = await fetch("http://localhost:5000/optimize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '服务器处理请求失败');
        }
        
        const data = await response.json();
        return data.optimizedText;
    } catch (error) {
        console.error('API 调用失败:', error);
        throw error;
    }
} 