$(function(){
  $('#btnCreateNewKey').click(function(){
    console.log('创建新密钥');
    $.ajax({
      method: 'post',  //get or post
      url: 'http://127.0.0.1:5000/api/v1/create_entropy',
      data: {},
      dataType: 'json',
    }).done(function(data){
      console.log(data);
      layer.msg('创建成功')
    }).fail(function(err){
      layer.alert('创建失败' + err);
    });
    appendKey({}, '#keyContainer');  // 创建成功后传入返回数据调用，此处示例
  })
  // 创建脚本
  $('#btnCreateScript').click(function(){
    console.log('创建脚本');
    $.ajax({
      method: 'get',  //get or post
      url: '/test',
      data: {},
      dataType: 'json',
    }).done(function(data){
      console.log(data);
      layer.msg('创建成功')
    }).fail(function(err){
      layer.alert('创建失败' + err);
    });
    appendKey({}, '#scriptContainer');
  })
  // 追加内容到页面
  function appendKey(data, domId) {
    var html = '<tr><td>xxxxxxxxxxxxxxxxx</td><td>xxxxxxxxxxxxxxx</td></tr>';
    $(domId).append(html);
  }

  // 发送
  $('#btnSendToSide').click(function(e){
    e.stopPropagation();
    e.preventDefault();
    var data = $('#formToSide').serializeArray();
    var obj = {};
    $.each(data, function () {
      obj[this.name] = this.value;
    });
    $.ajax({
      method: 'post',
      dataType: 'json',
      url: '',
      data: {data: JSON.stringify(obj)},
    }).done(function(res){
      console.log(res);
    }).fail(function(err) {
      layer.alert('err');
    });
  })
});