// index_v2.js

Page({
  data: {
    // ... (其他 data 字段不变)
    analysisWithTyping: {}, // 用于逐字打印的分析对象
    typingTimer: null // 用于清除定时器
  },

  // ... (其他生命周期和事件处理函数不变)

  getFortune() {
    // ... (请求逻辑不变)

    wx.request({
      // ... (url, method, data, timeout 不变)
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ 
            result: res.data,
            showResult: true 
          });
          this.runTypingEffect(res.data.analysis);
        } else {
          // ... (错误处理不变)
        }
      },
      // ... (fail, complete 不变)
    })
  },

  runTypingEffect(analysis) {
    this.clearTypingTimer(); // 先清除旧的定时器
    const categories = ['summary', 'study', 'career', 'love', 'health', 'wealth', 'social'];
    let charIndex = 0;
    let categoryIndex = 0;
    let currentCategory = categories[categoryIndex];
    let displayedAnalysis = {};

    const timer = setInterval(() => {
      const fullText = analysis[currentCategory];
      if (charIndex < fullText.length) {
        displayedAnalysis[currentCategory] = fullText.substring(0, charIndex + 1);
        this.setData({ analysisWithTyping: displayedAnalysis });
        charIndex++;
      } else {
        categoryIndex++;
        if (categoryIndex < categories.length) {
          currentCategory = categories[categoryIndex];
          charIndex = 0;
        } else {
          this.clearTypingTimer(); // 全部完成
        }
      }
    }, 50); // 每50毫秒打印一个字

    this.setData({ typingTimer: timer });
  },

  clearTypingTimer() {
    if (this.data.typingTimer) {
      clearInterval(this.data.typingTimer);
      this.setData({ typingTimer: null });
    }
  },

  closeResult() {
    this.clearTypingTimer();
    this.setData({ showResult: false, analysisWithTyping: {} });
  },

  onUnload() {
    this.clearTypingTimer(); // 页面卸载时确保清除定时器
  }
});
