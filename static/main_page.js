

function showDialog() {
  // 创建对话框
  var dialog = document.createElement("div");
  dialog.style.cssText = "position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); z-index: 999; display: flex; justify-content: center; align-items: center;";

  // 创建输入框
  var input = document.createElement("input");
  input.type = "text";
  input.placeholder = "请输入验证key";
  input.style.cssText = "width: 200px; height: 30px; margin-right: 10px;";

  // 创建确定按钮
  var confirmBtn = document.createElement("button");
  confirmBtn.innerText = "确定";
  confirmBtn.style.cssText = "width: 80px; height: 30px; background-color: #4CAF50; border: none; color: white; margin-right: 10px;";

  // 创建取消按钮
  var cancelBtn = document.createElement("button");
  cancelBtn.innerText = "取消";
  cancelBtn.style.cssText = "width: 80px; height: 30px; background-color: #f44336; border: none; color: white;";

  // 组装对话框
  dialog.appendChild(input);
  dialog.appendChild(confirmBtn);
  dialog.appendChild(cancelBtn);

  // 显示对话框
  document.body.appendChild(dialog);

  // 绑定事件
  confirmBtn.onclick = function() {
    var inputStr = input.value;
    var md5Str = "[your target md5]";
    var md5Input = hex_md5(inputStr);
    if (md5Input === md5Str) {
      dialog.style.display = "none";
      window.location.href = document.getElementById("chat").href;
    } else {
      showDialogError();
    }
  };

  cancelBtn.onclick = function() {
    dialog.style.display = "none";
  };
}

function showDialogError() {
  alert("验证key错误");
}

const sendBtn = document.getElementById('chat');
sendBtn.addEventListener('click', showDialog)