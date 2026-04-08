// index_v2.js

Page({
  data: {
    name: '',
    birthdate: '',
    mbtiRange: ['选择您的MBTI类型', 'ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'],
    mbtiIndex: 0,
    showResult: false,
    result: {},
    analysisWithTyping: {}, 
    typingTimer: null 
  },

  onNameInput(e) {
    this.setData({ name: e.detail.value });
  },

  onBirthdateChange(e) {
    this.setData({ birthdate: e.detail.value });
  },

  onMbtiChange(e) {
    this.setData({ mbtiIndex: e.detail.value });
  },

  getFortune() {
    if (!this.data.name || !this.data.birthdate || this.data.mbtiIndex == 0) {
      wx.showToast({ title: '请输入所有信息', icon: 'none' });
      return;
    }

    wx.showLoading({ title: '匹配天命中...' });

    const requestData = {
      name: this.data.name,
      birthdate: this.data.birthdate,
      mbti: this.data.mbtiRange[this.data.mbtiIndex]
    };

    const requestUrl = 'https://fortune-telling-app-lake.vercel.app/api/v1/divine';

    wx.request({
      url: requestUrl,
      method: 'POST',
      data: requestData,
      timeout: 15000,
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ result: res.data, showResult: true });
          this.runTypingEffect(res.data.analysis);
        } else {
          wx.showToast({ title: `服务返回错误: ${res.statusCode}`, icon: 'none' });
        }
      },
      fail: (err) => {
        wx.showToast({ title: `连接服务器失败，请稍后重试。`, icon: 'none', duration: 3000 });
      },
      complete: () => {
        wx.hideLoading();
      }
    })
  },

  runTypingEffect(analysis) {
    this.clearTypingTimer();
    const categories = ['summary', 'study', 'career', 'love', 'health', 'wealth', 'social'];
    let charIndex = 0;
    let categoryIndex = 0;
    let currentCategory = categories[categoryIndex];
    let displayedAnalysis = {};

    const timer = setInterval(() => {
      const fullText = analysis[currentCategory] || '';
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
          this.clearTypingTimer();
        }
      }
    }, 50);

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
    this.clearTypingTimer();
  }
});
