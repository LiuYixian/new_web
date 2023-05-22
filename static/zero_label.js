const container = document.getElementById('container');
const addButton = container.querySelector('.add');
const inputNameEls = container.querySelectorAll('.labels');
const inputDefinitionEls = container.querySelectorAll('.descs');
const resultsContainer = document.getElementById('results-container');
const label_text = document.getElementById('label_text');

addButton.addEventListener('click', () => {
  const newRow = document.createElement('div');
  newRow.className = 'row';
  newRow.innerHTML = `
    <div class="col col-1"><input class="labels" type="text" maxlength="8"></div>
    <div class="col col-2 "><textarea class="textarea descs"></textarea></div>
    <div class="col col-3"><button class="delete">删除</button></div>
  `;
  container.insertBefore(newRow, addButton.parentNode.parentNode);
});

container.addEventListener('click', e => {
  if (e.target.classList.contains('delete')) {
    e.target.parentNode.parentNode.remove();
  }
});

const textareas = document.querySelectorAll('.textarea');
function resizeTextarea(event) {
  const textarea = event.target;
  if (textarea.value.length > 25){
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
  }
  else{
      textarea.style.height = '1.8em';
  }
}

// 在绑定事件监听器之前对每个输入框运行一次 `resizeTextarea` 函数
for (const textarea of textareas) {
  resizeTextarea({target: textarea});
  textarea.addEventListener('input', resizeTextarea);
}

function getLabels() {
  const labels = {};
  for (let i = 0; i < inputNameEls.length; i++) {
    const name = inputNameEls[i].value;
    const definition = inputDefinitionEls[i].value;
    if (name) {
      labels[name] = definition;
    }
  }
  return labels;
}

const confirmBtn = document.getElementById("confirm-btn");
// 监听确定按钮的点击事件
confirmBtn.addEventListener("click", () => {
  resultsContainer.innerHTML = '';
  labels = getLabels();
  label_text_string = label_text.value
  const options = {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      labels: labels,
      label_text_string: label_text_string
    }),
  };
  fetch("/api/zero_label_api", options)
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
        x = 1;
      })

})
// result = getLabels()
// x=1