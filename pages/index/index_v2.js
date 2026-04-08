// index.js

Page({
  data: {
    name: '',
    birthdate: '',
    mbtiRange: ['选择您的MBTI类型', 'ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'],
    mbtiIndex: 0,
    showResult: false,
    result: {}
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
      wx.showToast({
        title: '请输入所有信息',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({
      title: '匹配天命中...',
    });

    const requestData = {
      name: this.data.name,
      birthdate: this.data.birthdate,
      mbti: this.data.mbtiRange[this.data.mbtiIndex]
    };

    const requestUrl = 'http://17.81.101.150:8000/api/v1/divine';

    console.log("即将发起请求，URL:", requestUrl);
    console.log("请求数据:", requestData);

    wx.request({
      url: requestUrl,
      method: 'POST',
      data: requestData,
      timeout: 5000, // 设置5秒超时
      success: (res) => {
        console.log("收到成功响应:", res);
        if (res.statusCode === 200) {
          this.setData({ 
            result: res.data,
            showResult: true 
          });
        } else {
          wx.showToast({
            title: `服务返回错误: ${res.statusCode}`,
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        console.error("请求失败:", err);
        wx.showToast({
          title: `连接服务器失败，请检查网络或服务是否开启。请求地址: ${requestUrl}`,
          icon: 'none',
          duration: 3000
        });
      },
      complete: () => {
        wx.hideLoading();
      }
    })
  },

  closeResult() {
    this.setData({ showResult: false });
  }
});
