document.getElementById('shakeButton').addEventListener('click', () => {
  const name = document.getElementById('nameInput').value;
  const birthdate = document.getElementById('birthdateInput').value;
  const mbti = document.getElementById('mbtiInput').value;

  if (!name || !birthdate || !mbti) {
    alert('请输入所有信息！');
    return;
  }

  // 隐藏主容器，准备显示结果
  document.querySelector('.container').style.display = 'none';

  // 模拟后端计算
  setTimeout(() => {
    const birthMonth = new Date(birthdate).getMonth();
    const fortuneIndex = birthMonth % fortunes.length;
    const result = fortunes[fortuneIndex];

    document.getElementById('resultFortune').textContent = result.fortune;
    
    const analysisContainer = document.getElementById('resultAnalysis');
    analysisContainer.innerHTML = ''; // 清空旧内容
    for (const key in result.analysis) {
      const p = document.createElement('p');
      p.textContent = result.analysis[key];
      analysisContainer.appendChild(p);
    }

    document.getElementById('resultCard').style.display = 'block';
  }, 1000);
});

document.getElementById('closeButton').addEventListener('click', () => {
  document.getElementById('resultCard').style.display = 'none';
  document.querySelector('.container').style.display = 'flex'; // 重新显示主容器
});
