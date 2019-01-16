$(function(){
  // 生成新熵
  $('#btnCreateNewKey').click(function(){
    console.log('创建新密钥');
    $.ajax({
      method: 'post',  //get or post
      url: 'http://127.0.0.1:5000/api/v1/create_new_key',
      data: {},
      dataType: 'json',
    }).done(function(data){
      console.log(data);
      layer.msg('创建成功')
      $('#txtEntropy').val(data.entropy)
      $('#txtMnemonics').val(data.mnemonic)
      $('#txtSeed').val(data.seed)
      $('#txtRootXprv').val(data.xprv)
      $('#txtRootXpub').val(data.xpub)
      $('#imgXprvQRCode').attr('src', 'data:image/jpg;base64,' + data.xprv_base64)
    }).fail(function(err){
      layer.alert('创建失败' + err);
    });
  })
  // 清除熵
  $('#btnResetKey').click(function(){
    console.log('清除');
    $('#txtEntropy').val('')
    $('#txtMnemonics').val('')
    $('#txtSeed').val('')
    $('#txtRootXprv').val('')
    $('#txtRootXpub').val('')
    $('#imgXprvQRCode').attr('src', 'data:image/jpg;base64,')
  })
  // 生成新地址
  $('#btnCreateNewAddress').click(function(){
    console.log('创建新密钥');
    $.ajax({
      method: 'post',  //get or post
      url: 'http://127.0.0.1:5000/api/v1/create_new_key',
      data: {},
      dataType: 'json',
    }).done(function(data){
      console.log(data);
      layer.msg('创建成功')
      $('#txtEntropy').val(data.entropy)
      $('#txtMnemonics').val(data.mnemonic)
      $('#txtSeed').val(data.seed)
      $('#txtRootXprv').val(data.xprv)
      $('#txtRootXpub').val(data.xpub)
      $('#imgXprvQRCode').attr('src', 'data:image/jpg;base64,' + data.xprv_base64)
    }).fail(function(err){
      layer.alert('创建失败' + err);
    });
  })
  // 清除地址
  $('#btnResetReceiver').click(function(){
    console.log('清除');
    $('#txtXpub').val('')
    $('#txtAccountIndex').val('')
    $('#txtAddressIndex').val('')
    $('#txtAddressPath').val('')
    $('#txtControlProgram').val('')
    $('#txtAddress').val('')
    $('#imgAddressQRCode').attr('src', 'data:image/jpg;base64,')
  })
});
