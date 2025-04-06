document.addEventListener('DOMContentLoaded', function() {
    const userSearch = document.getElementById('reply-user-search');
    const userResults = document.getElementById('reply-user-results');
    const receiverInput = document.getElementById('id_receiver');
    const form = document.getElementById('reply-form');
    
    if (!userSearch || !userResults || !receiverInput) return;

    function showDropdown() {
        userResults.style.display = 'block';
        userResults.style.position = 'absolute';
        userResults.style.left = '0';
        userResults.style.top = '100%';
        userResults.style.width = userSearch.offsetWidth + 'px';
        userResults.style.zIndex = '1000';
    }

    function hideDropdown() {
        userResults.style.display = 'none';
    }

    userSearch.addEventListener('input', function(e) {
        const query = e.target.value.replace('@', '').trim();
        
        if (query.length < 2) {
            hideDropdown();
            return;
        }
        
        fetch(`/search_users/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
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
                    userResults.innerHTML = '<a class="dropdown-item disabled">无匹配用户</a>';
                    showDropdown();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                hideDropdown();
            });
    });

    document.addEventListener('click', function(e) {
        if (!userSearch.contains(e.target) && !userResults.contains(e.target)) {
            hideDropdown();
        }
    });

    form.addEventListener('submit', function(e) {
        if (userSearch.value.startsWith('@') && !receiverInput.value) {
            e.preventDefault();
            alert('请从下拉菜单中选择有效的用户');
        }
    });
});