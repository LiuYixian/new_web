const sendBtn = document.getElementById('send-btn');


function load_role_config(role_label){
    var role_config = {
            "name": document.getElementById(role_label + '-name').value,
            "race": document.getElementById(role_label + '-race').value,
            "gender": document.getElementById(role_label + '-gender').value,
            "age": document.getElementById(role_label + '-age').value,
            "like": document.getElementById(role_label + '-like').value,
            "job": document.getElementById(role_label + '-job').value,
            "identity": document.getElementById(role_label + '-identity').value,
            "personality": document.getElementById(role_label + '-personality').value,
            "habit": document.getElementById(role_label + '-habit').value,
            "experience": document.getElementById(role_label + '-experience').value,
            "other": document.getElementById(role_label + '-other').value
        };
    return role_config
}

function load_other_config(){
    var other_config = {
        'role-relationship': document.getElementById('role-relationship').value,
        'role-feelings': document.getElementById('role-feelings').value,
        'conversation-scenario': document.getElementById('conversation-scenario').value,
        'important-experience': document.getElementById('important-experience').value,
    }
    return other_config
}

function push_role_config(role_label, config_dict){
            document.getElementById(role_label + '-name').value = config_dict['name'];
            document.getElementById(role_label + '-race').value = config_dict['race'];
            document.getElementById(role_label + '-gender').value = config_dict['gender'];
            document.getElementById(role_label + '-age').value = config_dict['age'];
            document.getElementById(role_label + '-like').value = config_dict['like'];
            document.getElementById(role_label + '-job').value = config_dict['job'];
            document.getElementById(role_label + '-identity').value = config_dict['identity'];
            document.getElementById(role_label + '-personality').value = config_dict['personality'];
            document.getElementById(role_label + '-habit').value = config_dict['habit'];
            document.getElementById(role_label + '-experience').value = config_dict['experience'];
            document.getElementById(role_label + '-other').value = config_dict['other'];
}



sessionStorage.setItem('key', 'value')
// Append user message to chat window

const messageList = document.querySelector('.messages');
function appendUserMessage(message) {
    const li = document.createElement('li');
    li.className = 'user-message';
    // li.innerHTML = `<p>${message}</p>`;
    li.innerHTML = marked.marked(message);
    messageList.appendChild(li);
    li.scrollIntoView({ behavior: 'smooth' });
}

const inputField = document.querySelector('#myTextarea');
//
inputField.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) { // 监听按下的键是否是 Enter ，同时不按下shift键
    event.preventDefault(); // 阻止默认行为，即阻止在文本框中直接输入回车
    sendBtn.click(); // 触发 "发送" 按钮的 click 事件
  }
});

conver_list = [

]
// 原始点击事件
sendBtn.addEventListener('click', () => {
    // 提取输入文本
    const inputElement = document.querySelector('.input-wrapper textarea');
    const inputText = inputElement.value;
    if (inputText === ''){
        alert('对话输入不可为空！')
        return
    }
    // 将输入文本显示在页面上
    appendUserMessage(inputText);

    // 定义输出文本框
    const textBox_output = document.createElement('textarea_output');
    textBox_output.className = 'response-text-box'; //输出文本框class
    messageList.appendChild(textBox_output);
    inputElement.value = ''; //清空输入框
    textBox_output.innerHTML = ''

    system_role_config = load_role_config('system') //提取系统角色配置
    user_role_config = load_role_config('user') //提取用户角色配置
    other_config = load_other_config() //提取其他配置

    // 限制历史对话长度
    // if (conver_list.length >= 20){
    //     conver_list = conver_list.slice(conver_list.length - 19)
    // }

    // conver_list.push({ role: 'user', content: inputText })

    // const message = [{ role: 'system', content: my_system_str }].concat(
    //     conver_list
    // );

    const data = {
        conver_list: conver_list ,
        inputText: inputText,
        system_role_config: system_role_config,
        user_role_config: user_role_config,
        other_config: other_config,

    };
    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    };
    try {
        fetch('/api/chat', options).then(response => {
          const reader = response.body.getReader();
          let temp = new Uint8Array();
          const decoder = new TextDecoder();
          (async function readChunks() {
            while (true) {
              const { done, value } = await reader.read(new Uint8Array(1));
              if (done) {
                break;
              }
              try {
                const chunk = decoder.decode(value);
                if (chunk.includes('Internal Server Error')){
                    textBox_output.innerHTML = '出现网络问题，请重试'
                    textBox_output.style.color = 'red';
                    textBox_output.style.fontSize = '10px';
                    return
                }
                console.log(chunk);
                textBox_output.innerHTML += chunk
              } catch {
                temp = new Uint8Array([...temp, ...value]);
                try {
                  const temp_str = decoder.decode(temp);
                  console.log(temp_str);
                  textBox_output.innerHTML += temp_str
                  temp = new Uint8Array();
                } catch (error) {
                  console.error(error);
                  textBox_output.innerHTML = '出现网络问题，请重试'
                    textBox_output.style.color = 'red';
                    textBox_output.style.fontSize = '10px';
                    return
                }
              }

            }
            conver_list.push({ role: 'assistant', content: textBox_output.innerHTML })
            // const saved = sessionStorage.getItem('key')
            //   textBox_output.innerHTML += saved
          })();
        }).catch(error => {
                    textBox_output.innerHTML = '出现网络问题，请重试'
                    textBox_output.style.color = 'red';
                    textBox_output.style.fontSize = '10px';
                    return
          console.error(error);
        });
    }
    catch{
        textBox_output.innerHTML = '出现网络问题，请重试'
            textBox_output.style.color = 'red';
            textBox_output.style.fontSize = '10px';
    }


});
// const my_system_str = '';
//
// 读取默认配置并存储到 sessionStorage



// 从 sessionStorage 中读取配置并显示在文本框中

const fixedText = "<p>网页功能仍在调试，试用过程中可能出现一些位置问题。目前使用作者的账号，只有单账号支持，峰值为1分钟内3次请求，如果出现较慢的情况可以等待或联系作者。为可能出现的问题提前致歉。</p>";
document.getElementById("fixed-text").innerHTML = fixedText;




// 对标记为textareas的组件进行高度初始化或者动态高度调整
const textareas = document.querySelectorAll('.textarea');
function resizeTextarea(event) {
  const textarea = event.target;
  if (textarea.value.length > 25){
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
  }
  else{
      textarea.style.height = '1.2em';
  }
}

// 在绑定事件监听器之前对每个输入框运行一次 `resizeTextarea` 函数
for (const textarea of textareas) {
  resizeTextarea({target: textarea});
  textarea.addEventListener('input', resizeTextarea);
}



$(document).ready(function() {

});

function role_config_mousedown() {
  // 共同的事件处理逻辑
    const userKeyTextbox = document.getElementById("user_key");
    var oldValue = $(this).data("oldValue");
    var select = $(this)
    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({'user_key': userKeyTextbox.value}),
    };
    fetch('/api/check_pre_save_role', options)
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        // var select = $(this);
        select.empty();
        select.append('<option value="other">请选择</option>');
        $.each(data, function(index, value) {
          select.append($('<option>').text(value).attr('value', value));
        });
        select.val(oldValue)
      })
      .catch(function(error) {
        console.error('获取选项列表失败:', error);
      });
}

function config_change(role_label, item){
    // 弹出确认对话框
    var newValue = item.val();
    var oldValue = item.data("oldValue");
    var result = confirm("是否用预设信息覆盖当前信息？");
    var select = item


    if (result) {
      // 获取当前下拉菜单值

      // 向服务端发送POST请求
      fetch('/api/get_role_config', {
          method: 'POST',
          body: JSON.stringify({ role_key: newValue }),
          headers: {
            'Content-Type': 'application/json'
          }
        })
          .then(response => response.json())
          .then(data => {
            // 根据服务端返回的dict结果进行其他设置
            select.data("oldValue", newValue);
            document.getElementById(role_label + '-name').value = data['name'];
            document.getElementById(role_label + '-race').value = data['race'];
            document.getElementById(role_label + '-gender').value = data['gender'];
            document.getElementById(role_label + '-age').value = data['age'];
            document.getElementById(role_label + '-like').value = data['like'];
            document.getElementById(role_label + '-job').value = data['job'];
            document.getElementById(role_label + '-identity').value = data['identity'];
            document.getElementById(role_label + '-personality').value = data['personality'];
            document.getElementById(role_label + '-habit').value = data['habit'];
            document.getElementById(role_label + '-experience').value = data['experience'];
            document.getElementById(role_label + '-other').value = data['other'];
            // {age: '18岁', experience: '往生堂第十八代堂主', gender: '女性', habit: '"吃好喝好一路走好","本堂主"', identity: '往生堂堂主（往生堂是璃月最大的殡葬机构）', …}
            x=1
          })
          .catch(error => console.error(error));
    } else {
        x=1
        item.val(oldValue)
      // 取消操作
    }
}

function config_change_user(){
    config_change('user', $("#user_config"))
}

function config_change_system(){
    config_change('system', $("#system_config"))
}
$(document).ready(function() {
  // 在下拉菜单选择变更时触发
  var $systemMenu = $("#system_config");
  var oldValue = $systemMenu.val(); // 保存旧的下拉菜单值
  $systemMenu.data("oldValue", oldValue);

  var $userMenu = $("#user_config");
  var oldValue = $userMenu.val(); // 保存旧的下拉菜单值
  $userMenu.data("oldValue", oldValue);

  $('#system_config').on('mousedown', role_config_mousedown);
  $('#user_config').on('mousedown', role_config_mousedown);

  $("#system_config").change(config_change_system);
  $("#user_config").change(config_change_user);
});

// 获取按钮元素
let user_key_check_btn = document.querySelector('#user_key_check');

// 给按钮绑定点击事件
user_key_check_btn.addEventListener('click', function() {

  // 获取文本框元素和输入内容
  let txtBox = document.querySelector('#user_key');
  let userKey = txtBox.value;

  // 发送POST请求
  fetch('/api/check_user_key', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({'user_key': userKey})
  })
  .then(response => response.text())
  .then(result => {
    // 根据返回结果弹出对话框提示信息
    if (result === 'pass') {
      alert('该 user-key 尚未被使用，可以使用。');
    } else if (result === 'conflict') {
      alert('该 user-key 已经存在，如果并非由您建立，则建议另外选择一个 user-key。');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

// 获取按钮元素
let system_role_save_btn = document.querySelector('#system_role_save');
let user_role_save_btn = document.querySelector('#user_role_save');

function role_save(role_label){
  const userKeyTextbox = document.getElementById("user_key");
  const roleNameTextbox = document.getElementById(role_label+"-" + role_label + "_rol_save_name");

  const postData = {
    user_key: userKeyTextbox.value,
    role_name: roleNameTextbox.value
  };

  // Send post request to check if role key already exists
  fetch("/api/check_role_key", {
    method: "POST",
      headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(postData)
  })
  .then(response => response.text())
  .then(data => {
    if (data === "no user_key"){
        alert("user-key为空，请填入个人user-key");
        return
    }
    else if (data === "no role_name"){
        alert("角色保存名字为空，请填入要保存的角色名称");
        return
    }
    else if (data === "no") {
      ; // Role key does not exist, do nothing
    }
    else if (data === "exist") {
      // Show confirmation dialog if role key already exists
      const confirmDialog = confirm("该角色名已经存在，是否覆盖？");
      if (!confirmDialog) {
        return; // User clicked cancel, do nothing
      }
    }
    var role_config = {
            "name": document.getElementById(role_label + '-name').value,
            "race": document.getElementById(role_label + '-race').value,
            "gender": document.getElementById(role_label + '-gender').value,
            "age": document.getElementById(role_label + '-age').value,
            "like": document.getElementById(role_label + '-like').value,
            "job": document.getElementById(role_label + '-job').value,
            "identity": document.getElementById(role_label + '-identity'),
            "personality": document.getElementById(role_label + '-personality').value,
            "habit": document.getElementById(role_label + '-habit').value,
            "experience": document.getElementById(role_label + '-experience').value,
            "other": document.getElementById(role_label + '-other').value
        }; // Construct the role configuration object
    var data = {
        user_key: userKeyTextbox.value,
        role_name: roleNameTextbox.value,
        role_config: role_config
    }
    // Send post request to save role key
    fetch("/api/save_role_key", {
      method: "POST",
        headers: {
      'Content-Type': 'application/json'
    },
      body: JSON.stringify(data)
    })
    .then(response => response.text())
    .then(data => {
      if (data === "success") {
        alert("角色保存成功！");
      }
      else {
        alert("角色保存失败，请重试或联系作者。");
      }
    });
  });
}
function role_save_system(){
    role_save('system')
}
function role_save_user(){
    role_save('user')
}
system_role_save_btn.addEventListener('click', role_save_system);
user_role_save_btn.addEventListener('click', role_save_user);