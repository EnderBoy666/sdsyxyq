document.addEventListener('DOMContentLoaded', function() {
    const userSearch = document.getElementById('user-search');
    const userResults = document.getElementById('user-results');
    const receiverInput = document.getElementById('id_receiver');
    let debounceTimer;

    // 显示下拉菜单的函数
    function showDropdown() {
        userResults.style.display = 'block';
        userResults.style.position = 'absolute';
        userResults.style.zIndex = '1000';
        userResults.style.width = userSearch.offsetWidth + 'px';
    }

    // 隐藏下拉菜单的函数
    function hideDropdown() {
        userResults.style.display = 'none';
    }

    userSearch.addEventListener('input', function(e) {
        clearTimeout(debounceTimer);
        const query = e.target.value.replace('@', '').trim();
        
        if (query.length < 2) {
            hideDropdown();
            return;
        }
        
        debounceTimer = setTimeout(() => {
            fetch(`/search_users/?q=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(data => {
                    if (data.length > 0) {
                        userResults.innerHTML = '';
                        data.forEach(user => {
                            const item = document.createElement('a');
                            item.className = 'dropdown-item';
                            item.href = '#';
                            item.textContent = user.username;
                            item.dataset.userId = user.id;
                            item.addEventListener('click', function(e) {
                                e.preventDefault();
                                userSearch.value = `@${user.username}`;
                                receiverInput.value = user.id;
                                hideDropdown();
                            });
                            userResults.appendChild(item);
                        });
                        showDropdown();
                    } else {
                        hideDropdown();
                    }
                })
                .catch(error => {
                    console.error('Error fetching users:', error);
                    hideDropdown();
                });
        }, 300);
    });

    // 点击其他地方关闭下拉菜单
    document.addEventListener('click', function(e) {
        if (!userSearch.contains(e.target) && !userResults.contains(e.target)) {
            hideDropdown();
        }
    });

    // 输入框获得焦点时显示已有结果
    userSearch.addEventListener('focus', function() {
        if (userResults.children.length > 0) {
            showDropdown();
        }
    });
});