//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    needAuth: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  onLoad: function (options) {
    this.next_url = options.next_url || '/';

    wx.login({
      success: res => {
        this.code = res.code;

        wx.getSetting({
          success: res => {
            if (res.authSetting['scope.userInfo']) {
              this.getUserInfo();
            }
            else {
              this.setData({
                needAuth: true
              });
            }
          }
        });
      }
    });
  },
  login: function () {
    var url = app.domain + '/login/miniapp/?';
    url += 'code=' + encodeURIComponent(this.code) + '&';
    url += 'encrypted_data=' + encodeURIComponent(this.encrypted_data) + '&';
    url += 'iv=' + encodeURIComponent(this.iv) + '&';
    url += 'next=' + encodeURIComponent(this.next_url);

    wx.request({
      url: url,
      success: res => {
        if (res.statusCode == 200) {
          var next_url = res.data.next_url;
          var token = res.data.token;
          console.log(next_url);
          console.log(token);

          var url = '/pages/index/index?token=' + token + '&next_url=' + next_url;
          wx.redirectTo({
            url: url,
          })
        }
        else {
          console.log('fail login', url, res);
          this.showLoginError();
        }
      },
      fail: res => {
        console.log('fail request', res);
        this.showLoginError();
      }
    })
  },
  getUserInfo: function () {
    this.setData({
      needAuth: false
    });
    wx.getUserInfo({
      success: res => {
        this.encrypted_data = res.encryptedData;
        this.iv = res.iv;
        this.login();
      },
      fail: res => {
        console.log('fail getUserInfo', res);
        this.showLoginError();
      }
    })
  },
  showLoginError: function () {
    this.setData({
      needAuth: true
    });
    wx.showModal({
      title: '登录失败，请重新授权',
    });
  }
})
