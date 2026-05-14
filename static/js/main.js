document.addEventListener('DOMContentLoaded', () => {
    const taskItems = document.querySelectorAll('.task-item');

    taskItems.forEach(item => {
        const titleSpan = item.querySelector('.task-title');
        const inputField = item.querySelector('.task-edit-input');
        const taskId = item.dataset.id;

        // 當點擊文字時，切換成輸入框
        titleSpan.addEventListener('click', () => {
            titleSpan.classList.add('hidden');
            inputField.classList.remove('hidden');
            inputField.focus();
            
            // 將游標移到文字最後面
            const val = inputField.value;
            inputField.value = '';
            inputField.value = val;
        });

        // 取消編輯模式（恢復原本文字）
        const cancelEdit = () => {
            inputField.classList.add('hidden');
            titleSpan.classList.remove('hidden');
            inputField.value = titleSpan.textContent; // 恢復原值
        };

        // 儲存修改內容
        const saveEdit = async () => {
            const newTitle = inputField.value.trim();
            const oldTitle = titleSpan.textContent;

            // 如果沒有改變或為空，則取消編輯
            if (newTitle === oldTitle || newTitle === '') {
                cancelEdit();
                return;
            }

            // 加入 saving 動畫效果與鎖定
            inputField.classList.add('saving');
            inputField.disabled = true;

            try {
                const response = await fetch(`/api/tasks/${taskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ title: newTitle })
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    // 更新成功
                    titleSpan.textContent = result.title;
                    inputField.value = result.title;
                    inputField.classList.add('hidden');
                    titleSpan.classList.remove('hidden');
                } else {
                    // 更新失敗
                    alert(result.error || '儲存失敗，請重試');
                    cancelEdit();
                }
            } catch (error) {
                console.error('Error updating task:', error);
                alert('發生網路錯誤，請重試');
                cancelEdit();
            } finally {
                inputField.classList.remove('saving');
                inputField.disabled = false;
            }
        };

        // 按下 Enter 儲存，按下 Escape 取消
        inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                saveEdit();
            } else if (e.key === 'Escape') {
                cancelEdit();
            }
        });

        // 點擊輸入框外（失去焦點）時儲存
        inputField.addEventListener('blur', () => {
            // 使用 setTimeout 避免與其他按鈕點擊事件衝突
            setTimeout(() => {
                if (!inputField.classList.contains('hidden')) {
                     saveEdit();
                }
            }, 100);
        });
    });
});
