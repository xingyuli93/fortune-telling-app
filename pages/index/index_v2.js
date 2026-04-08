// index_v2.js

Page({
  data: {
    // ... (data 字段不变)
  },

  // ... (onNameInput, onBirthdateChange, onMbtiChange 不变)

  startShake() {
    if (!this.data.name || !this.data.birthdate || this.data.mbtiIndex == 0) {
      wx.showToast({ title: '请输入所有信息', icon: 'none' });
      return;
    }
    this.setData({ showShake: true, showResult: false }); // 确保主界面和结果页都隐藏
    this.listenShake();
  },

  // ... (listenShake, getFortune, runTypingEffect, clearTypingTimer, closeResult, onUnload 逻辑不变)
});
