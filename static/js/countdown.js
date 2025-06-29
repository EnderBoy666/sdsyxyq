// 改进的倒计时功能，支持时区设置
function initCountdown(elementId, targetDateStr, timezoneOffset = 0) {
    const element = document.getElementById(elementId);
    
    // 检查元素是否存在
    if (!element) {
        console.error('未找到倒计时元素:', elementId);
        return;
    }
    
    // 尝试多种日期解析方式以提高兼容性
    let targetDate;
    
    // 尝试ISO格式
    targetDate = new Date(targetDateStr);
    if (isNaN(targetDate.getTime())) {
        // 尝试本地化格式
        const parts = targetDateStr.split(/[- :T]/);
        if (parts.length >= 6) {
            targetDate = new Date(
                parseInt(parts[0]),
                parseInt(parts[1]) - 1, // 月份从0开始
                parseInt(parts[2]),
                parseInt(parts[3]),
                parseInt(parts[4]),
                parseInt(parts[5])
            );
        }
    }
    
    // 应用时区偏移
    if (!isNaN(targetDate.getTime()) && timezoneOffset !== 0) {
        targetDate = new Date(targetDate.getTime() + timezoneOffset * 60 * 60 * 1000);
    }
    
    // 检查日期是否有效
    if (isNaN(targetDate.getTime())) {
        console.error('无效的目标日期:', targetDateStr);
        element.innerHTML = "日期格式错误";
        return;
    }
    
    console.log('倒计时目标日期:', targetDate.toLocaleString());
    
    function updateCountdown() {
        const now = new Date();
        const diff = targetDate - now;
        
        if (diff <= 0) {
            element.innerHTML = "愿君畅行";
            return;
        }
        
        // 计算天、时、分、秒
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        // 格式化显示，确保两位数
        const formatNumber = (num) => num.toString().padStart(2, '0');
        
        element.innerHTML = `
            <div class="d-flex justify-content-center">
                <div class="px-3 py-2 bg-white text-info rounded mr-2">
                    <div class="text-2xl font-bold">${days}</div>
                    <div class="text-xs">天</div>
                </div>
                <div class="px-3 py-2 bg-white text-info rounded mr-2">
                    <div class="text-2xl font-bold">${formatNumber(hours)}</div>
                    <div class="text-xs">时</div>
                </div>
                <div class="px-3 py-2 bg-white text-info rounded mr-2">
                    <div class="text-2xl font-bold">${formatNumber(minutes)}</div>
                    <div class="text-xs">分</div>
                </div>
                <div class="px-3 py-2 bg-white text-info rounded">
                    <div class="text-2xl font-bold">${formatNumber(seconds)}</div>
                    <div class="text-xs">秒</div>
                </div>
            </div>
        `;
        
        setTimeout(updateCountdown, 1000);
    }
    
    // 立即更新一次，然后开始循环
    updateCountdown();
}

// 初始化日期时间显示
function initDateTime(elementId) {
    const element = document.getElementById(elementId);
    
    if (!element) {
        console.error('未找到日期时间元素:', elementId);
        return;
    }
    
    function updateDateTime() {
        const now = new Date();
        element.textContent = now.toLocaleString();
        setTimeout(updateDateTime, 1000);
    }
    
    updateDateTime();
}