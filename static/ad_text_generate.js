// 获取DOM节点
// const materialInput = document.getElementById("material");
const gameNameInput = document.getElementById("game-name");
const gameIntroInput = document.getElementById("game-intro");
const channelSelect = document.getElementById("channel");
const purposeInput = document.getElementById("purpose");
const wordCountInput = document.getElementById("word-count");
const confirmBtn = document.getElementById("confirm-btn");
const resultsDiv = document.querySelector(".results");
const resultsContainer = document.getElementById('results-container');
resultsDiv.style.whiteSpace = 'pre-line';

// 监听确定按钮的点击事件
confirmBtn.addEventListener("click", () => {

//   const results = {
//   'Result 1': 'This is a single line description for Result 1',
//   'Result 2': 'This is a multi-line description for Result 2. There are a lot of words here, so it is going to wrap onto multiple lines. This is perfectly fine, because we have set the word-wrap property to break-word in our CSS.',
//   'Result 3': 'This is a single line description for Result 3',
//   'Result 4': 'This is a multi-line description for Result 4. There are a lot of words here, so it is going to wrap onto multiple lines. This is perfectly fine, because we have set the word-wrap property to break-word in our CSS.',
//   'Result 5': 'This is a single line description for Result 5'
// };

  resultsContainer.innerHTML = '';

// for (const [title, description] of Object.entries(results)) {
//   const resultElement = document.createElement('div');
//   resultElement.classList.add('result');
//   const titleElement = document.createElement('div');
//   titleElement.classList.add('result-title');
//   titleElement.textContent = title;
//   const descriptionElement = document.createElement('div');
//   descriptionElement.classList.add('result-description');
//   descriptionElement.textContent = description;
//   resultElement.appendChild(titleElement);
//   resultElement.appendChild(descriptionElement);
//   resultsContainer.appendChild(resultElement);
// }
  if (gameNameInput.value === ''){
    alert('请提供要服务的游戏名称')
    return
  }
  resultsDiv.innerHTML = '正在进行分析，请稍等';

  // 获取各个输入框的值
  const input = {
    'text': '',
    'name': gameNameInput.value,
    'intro': gameIntroInput.value,
    'channel': channelSelect.value,
    'motivation': purposeInput.value,
    'num_limit': wordCountInput.value,
  };
   // resultsDiv.innerHTML = '正在进行分析';
  // 发送 AJAX 请求到服务端 API
  const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    };
  fetch("/api/response", options)
  .then(response => response.json())
  .then(data => {
    // 解析返回的数据并生成HTML代码
    let resultHtml = "";
    for (const [key, value] of Object.entries(data)) {
      // resultHtml += `<div><strong>${key}</strong>: ${value}</div>`;
      const resultElement = document.createElement('div');
      resultElement.classList.add('result');
      const titleElement = document.createElement('div');
      titleElement.classList.add('result-title');
      titleElement.textContent = key;
      const descriptionElement = document.createElement('div');
      descriptionElement.classList.add('result-description');
      descriptionElement.style.whiteSpace = 'pre-line';
      descriptionElement.innerHTML = value;
      resultElement.appendChild(titleElement);
      resultElement.appendChild(descriptionElement);
      resultsContainer.appendChild(resultElement);
    }

    resultsDiv.innerHTML = '分析完成';

    // 插入生成的HTML代码到结果栏

  })
  .catch(error => {
    console.error("请求出错：", error);
    resultsDiv.innerHTML = '分析出错，请重试或者联系作者';
  });
});

