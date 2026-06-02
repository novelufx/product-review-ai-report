// EduAI Copilot 交互逻辑

document.addEventListener('DOMContentLoaded', function() {

    // ============================================
    // 导航栏功能
    // ============================================

    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    // 移动端菜单切换
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }

    // 点击导航链接关闭菜单
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });

    // 滚动时改变导航栏样式
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });

    // 高亮当前区域对应的导航链接
    const sections = document.querySelectorAll('section[id]');

    function highlightNavLink() {
        var scrollY = window.pageYOffset;

        sections.forEach(function(section) {
            var sectionHeight = section.offsetHeight;
            var sectionTop = section.offsetTop - 100;
            var sectionId = section.getAttribute('id');

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNavLink);


    // ============================================
    // 图表初始化
    // ============================================

    // 使用场景柱状图
    var scenarioCtx = document.getElementById('scenarioChart');
    if (scenarioCtx) {
        new Chart(scenarioCtx, {
            type: 'bar',
            data: {
                labels: ['概念解释', '资料总结', '考试复习', '作业辅助', '编程学习', '论文阅读'],
                datasets: [{
                    label: '使用频率',
                    data: [72, 68, 63, 55, 47, 42],
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb',
                        '#f5576c',
                        '#4facfe',
                        '#43e97b'
                    ],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: '使用场景分布',
                        font: {
                            size: 16
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // 痛点分析图表
    var painPointsCtx = document.getElementById('painPointsChart');
    if (painPointsCtx) {
        new Chart(painPointsCtx, {
            type: 'bar',
            data: {
                labels: ['AI 答案不稳定', '不会写 Prompt', '缺少课程上下文', '资料分散', '复习计划难坚持', '难判断是否掌握'],
                datasets: [{
                    label: '提及人数',
                    data: [72, 67, 61, 58, 52, 49],
                    backgroundColor: [
                        '#ff4d4f',
                        '#ff7a45',
                        '#ffa940',
                        '#ffc53d',
                        '#ffec3d',
                        '#bae637'
                    ],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: '痛点分析（提及人数）',
                        font: {
                            size: 16
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // 竞品能力雷达图
    var competitorRadarCtx = document.getElementById('competitorRadarChart');
    if (competitorRadarCtx) {
        new Chart(competitorRadarCtx, {
            type: 'radar',
            data: {
                labels: ['知识解释', '长文档处理', '中文能力', '学习计划', '资料整理', '交互体验', '免费可用性', '可信度'],
                datasets: [
                    {
                        label: 'ChatGPT',
                        data: [9, 8, 8, 8, 7, 9, 7, 7],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2
                    },
                    {
                        label: 'Kimi',
                        data: [8, 10, 9, 7, 8, 8, 9, 8],
                        borderColor: '#764ba2',
                        backgroundColor: 'rgba(118, 75, 162, 0.1)',
                        borderWidth: 2
                    },
                    {
                        label: '豆包',
                        data: [8, 7, 9, 8, 7, 9, 9, 7],
                        borderColor: '#f5576c',
                        backgroundColor: 'rgba(245, 87, 108, 0.1)',
                        borderWidth: 2
                    },
                    {
                        label: '通义千问',
                        data: [8, 8, 9, 8, 7, 8, 8, 7],
                        borderColor: '#faad14',
                        backgroundColor: 'rgba(250, 173, 20, 0.1)',
                        borderWidth: 2
                    },
                    {
                        label: 'Notion AI',
                        data: [7, 7, 7, 6, 10, 8, 6, 7],
                        borderColor: '#52c41a',
                        backgroundColor: 'rgba(82, 196, 26, 0.1)',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 10,
                        ticks: {
                            stepSize: 2
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // 计算竞品综合平均分
    var competitorScores = {
        chatgpt: [9, 8, 8, 8, 7, 9, 7, 7],
        kimi: [8, 10, 9, 7, 8, 8, 9, 8],
        doubao: [8, 7, 9, 8, 7, 9, 9, 7],
        tongyi: [8, 8, 9, 8, 7, 8, 8, 7],
        notion: [7, 7, 7, 6, 10, 8, 6, 7]
    };

    function calculateAverage(scores) {
        var sum = scores.reduce(function(a, b) { return a + b; }, 0);
        return (sum / scores.length).toFixed(1);
    }

    // 更新平均分显示
    var avgChatgpt = document.getElementById('avg-chatgpt');
    var avgKimi = document.getElementById('avg-kimi');
    var avgDoubao = document.getElementById('avg-doubao');
    var avgTongyi = document.getElementById('avg-tongyi');
    var avgNotion = document.getElementById('avg-notion');

    if (avgChatgpt) avgChatgpt.textContent = calculateAverage(competitorScores.chatgpt);
    if (avgKimi) avgKimi.textContent = calculateAverage(competitorScores.kimi);
    if (avgDoubao) avgDoubao.textContent = calculateAverage(competitorScores.doubao);
    if (avgTongyi) avgTongyi.textContent = calculateAverage(competitorScores.tongyi);
    if (avgNotion) avgNotion.textContent = calculateAverage(competitorScores.notion);

    // 功能优先级图表
    var priorityCtx = document.getElementById('priorityChart');
    if (priorityCtx) {
        new Chart(priorityCtx, {
            type: 'doughnut',
            data: {
                labels: ['P0 核心功能', 'P1 重要功能', 'P2 扩展功能'],
                datasets: [{
                    data: [3, 2, 1],
                    backgroundColor: [
                        '#667eea',
                        '#faad14',
                        '#52c41a'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: '功能优先级分布',
                        font: {
                            size: 16
                        }
                    }
                }
            }
        });
    }


    // ============================================
    // Prompt 标签页切换
    // ============================================

    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var tabId = this.getAttribute('data-tab');

            // 移除所有 active 状态
            tabButtons.forEach(function(btn) {
                btn.classList.remove('active');
            });
            tabContents.forEach(function(content) {
                content.classList.remove('active');
            });

            // 添加当前 active 状态
            this.classList.add('active');
            document.getElementById('tab-' + tabId).classList.add('active');
        });
    });


    // ============================================
    // AI 对话演示
    // ============================================

    var chatMessages = document.getElementById('chatMessages');
    var userInput = document.getElementById('userInput');
    var sendButton = document.getElementById('sendButton');
    var demoButtons = document.querySelectorAll('.demo-btn');

    // 演示场景数据
    var demoScenarios = {
        note: {
            user: '帮我整理一下今天学的微积分笔记',
            ai: '好的，我来帮你整理。\n\n**微积分导数知识总结**\n\n**核心概念：**\n- 导数描述函数在某一点的变化速度\n- 几何意义：曲线在该点的切线斜率\n\n**关键公式：**\n- (x^n)\' = nx^(n-1)\n- (sin x)\' = cos x\n\n**学习建议：**\n- 先理解几何意义，再记公式\n- 多做求导练习'
        },
        concept: {
            user: '什么是机器学习中的"过拟合"？',
            ai: '我来用简单的方式解释。\n\n**通俗类比：**\n就像学生只背答案不理解原理，考试遇到新题就不会了。\n\n**技术定义：**\n模型在训练数据上表现很好，但在新数据上表现差。\n\n**实际例子：**\n训练识别猫的模型，只用家猫图片训练，遇到野猫就认不出来了。\n\n**怎么避免：**\n- 增加训练数据的多样性\n- 使用正则化技术'
        },
        plan: {
            user: '我下周要考高数，还有 5 章没复习，每天能学 3 小时',
            ai: '好的，我来帮你安排复习计划。\n\n**Day 1：函数与极限（3 小时）**\n- 上午：复习函数概念（1.5 小时）\n- 下午：复习极限（1.5 小时）\n\n**Day 2：导数（3 小时）**\n- 上午：复习导数定义和公式（1.5 小时）\n- 下午：复习求导法则（1.5 小时）\n\n**Day 3：积分（3 小时）**\n- 上午：复习不定积分（1.5 小时）\n- 下午：复习定积分（1.5 小时）\n\n**复习建议：**\n- 每天先看笔记，再做题\n- 整理错题，考前重点看'
        }
    };

    // 添加消息到聊天窗口
    function addMessage(content, isUser) {
        var messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + (isUser ? 'user-message' : 'ai-message');

        var contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // 处理换行
        var formattedContent = content.replace(/\n/g, '<br>');
        contentDiv.innerHTML = formattedContent;

        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);

        // 滚动到底部
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // 发送消息
    function sendMessage() {
        var message = userInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        userInput.value = '';

        // 模拟 AI 响应
        setTimeout(function() {
            var response = generateResponse(message);
            addMessage(response, false);
        }, 1000);
    }

    // 生成 AI 响应
    function generateResponse(message) {
        var lowerMessage = message.toLowerCase();

        if (lowerMessage.includes('笔记') || lowerMessage.includes('整理')) {
            return demoScenarios.note.ai;
        } else if (lowerMessage.includes('什么是') || lowerMessage.includes('解释')) {
            return demoScenarios.concept.ai;
        } else if (lowerMessage.includes('计划') || lowerMessage.includes('复习')) {
            return demoScenarios.plan.ai;
        } else {
            return '我是 EduAI Copilot，你的 AI 学习助手。我可以帮你：\n\n- 整理课堂笔记\n- 解释复杂概念\n- 制定学习计划\n- 分析错题原因\n\n请告诉我你需要什么帮助？';
        }
    }

    // 发送按钮点击事件
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }

    // 回车发送
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // 演示按钮点击事件
    demoButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var scenario = this.getAttribute('data-scenario');
            var demo = demoScenarios[scenario];

            if (demo) {
                // 清空聊天记录
                chatMessages.innerHTML = '';

                // 添加欢迎消息
                addMessage('你好！我是 EduAI Copilot，你的 AI 学习助手。\n\n我可以帮你：\n- 整理课堂笔记\n- 解释复杂概念\n- 制定学习计划\n- 分析错题原因\n\n请告诉我你需要什么帮助？', false);

                // 添加用户消息
                setTimeout(function() {
                    addMessage(demo.user, true);

                    // 添加 AI 响应
                    setTimeout(function() {
                        addMessage(demo.ai, false);
                    }, 1000);
                }, 500);
            }
        });
    });


    // ============================================
    // 复制 Prompt 功能
    // ============================================

    window.copyPrompt = function(button) {
        var codeBlock = button.closest('.prompt-code-block');
        var codeContent = codeBlock.querySelector('.code-content');
        var text = codeContent.textContent;

        navigator.clipboard.writeText(text).then(function() {
            var originalText = button.textContent;
            button.textContent = '已复制';
            button.style.background = '#52c41a';
            button.style.color = '#fff';

            setTimeout(function() {
                button.textContent = originalText;
                button.style.background = '#3d3d3d';
                button.style.color = '#9da5b4';
            }, 2000);
        }).catch(function() {
            // Fallback for older browsers
            var textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);

            var originalText = button.textContent;
            button.textContent = '已复制';
            button.style.background = '#52c41a';
            button.style.color = '#fff';

            setTimeout(function() {
                button.textContent = originalText;
                button.style.background = '#3d3d3d';
                button.style.color = '#9da5b4';
            }, 2000);
        });
    };


    // ============================================
    // 平滑滚动
    // ============================================

    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });


    // ============================================
    // 页面加载动画
    // ============================================

    // 为卡片添加渐入效果
    var observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // 观察所有卡片
    document.querySelectorAll('.content-card, .user-card, .scenario-item, .opportunity-card, .feature-card, .weakness-item, .metric-card, .roadmap-phase, .quote-card').forEach(function(card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

});
