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
    typingTimer: null,
    showShake: false,
    isShaking: false,
    isStickFalling: false
  },

  onNameInput(e) { this.setData({ name: e.detail.value }); },
  onBirthdateChange(e) { this.setData({ birthdate: e.detail.value }); },
  onMbtiChange(e) { this.setData({ mbtiIndex: e.detail.value }); },

  startShake() {
    if (!this.data.name || !this.data.birthdate || this.data.mbtiIndex == 0) {
      wx.showToast({ title: '请输入所有信息', icon: 'none' });
      return;
    }
    this.setData({ showShake: true });
    this.listenShake();
  },

  listenShake() {
    let shakeCount = 0;
    wx.startAccelerometer({
      interval: 'ui',
      success: () => {
        wx.onAccelerometerChange((res) => {
          if (Math.abs(res.x) > 1 || Math.abs(res.y) > 1 || Math.abs(res.z) > 1) {
            shakeCount++;
            this.setData({ isShaking: true });
            if (shakeCount > 5) { // 摇晃几次后触发
              wx.stopAccelerometer();
              this.setData({ isShaking: false, isStickFalling: true });
              setTimeout(() => {
                this.setData({ showShake: false });
                this.getFortune();
              }, 1000); // 掉落动画结束后获取结果
            }
          }
        });
      }
    });
  },

  getFortune() {
    wx.showLoading({ title: '匹配天命中...' });
    // ... (wx.request 逻辑保持不变)
  },

  // ... (runTypingEffect, clearTypingTimer, closeResult, onUnload 逻辑保持不变)
});
