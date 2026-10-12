"""A short prerequisite bridge, in both languages."""
ROWS=[
('先会这几个符号，再开始做题','Learn these symbols before your first problem',
'不用一次看完整章。每次只选一个知识点、一道人能跟上的题：先说出要找什么，再做第一步，算完就检查。遇到没学过的求导或积分，先回到下面对应的小卡片。',
'Work on one idea and one manageable problem at a time. Say what you need to find, take the first step, and check the result. If derivatives or integrals are unfamiliar, start with the small cards below.'),
('复数：把一个数写成两个方向','Complex numbers: two directions',
'写成 $z=x+iy$ 时，$x$ 是实部，$y$ 是虚部，$i^2=-1$。把它想成平面上的点 $(x,y)$；长度是 $|z|=\\sqrt{x^2+y^2}$。\n\n例如 $z=3+4i$，对应点 $(3,4)$，长度为 $5$。先能从表达式读出这三件事，就可以开始学极形式。',
'In $z=x+iy$, $x$ is the real part, $y$ the imaginary part, and $i^2=-1$. Picture the point $(x,y)$; its distance from the origin is $|z|=\\sqrt{x^2+y^2}$.\n\nFor $z=3+4i$, the point is $(3,4)$ and the distance is $5$. Practice identifying these three quantities before moving to polar form.'),
('导数与偏导：每次只让一个量变化','Derivatives: vary one quantity at a time',
'$f\\prime(x)$ 表示函数随 $x$ 变化有多快。幂函数的规则是 $(x^n)\\prime=nx^{n-1}$。\n\n$u_x$ 或 $\\partial u/\\partial x$ 是对 $x$ 求偏导：把其他变量暂时当常数。若 $u=x^2y+3y$，则 $u_x=2xy$，$u_y=x^2+3$。写 $u_{xx}$ 就是再对 $x$ 求一次偏导，得到 $2y$。',
'$f\\prime(x)$ measures how fast a function changes with $x$. For a power, $(x^n)\\prime=nx^{n-1}$.\n\n$u_x$, or $\\partial u/\\partial x$, means differentiate with respect to $x$ while holding other variables constant. For $u=x^2y+3y$, we get $u_x=2xy$ and $u_y=x^2+3$. Differentiating again gives $u_{xx}=2y$.'),
('积分：先找原函数，再代上下限','Integrals: find an antiderivative, then use the limits',
'最基本的一步是 $\\int x^n\\,dx=x^{n+1}/(n+1)+C$，条件是 $n\\ne-1$。定积分再做“上限值减下限值”。\n\n例如 $\\int_0^1 2x\\,dx=[x^2]_0^1=1$。碰到乘积先想分部积分，碰到内层函数及其导数先想换元；网站中的完整解析会展示具体怎么选。',
'The power rule is $\\int x^n\\,dx=x^{n+1}/(n+1)+C$, for $n\\ne-1$. For a definite integral, evaluate at the upper limit and subtract the value at the lower limit.\n\nFor example, $\\int_0^1 2x\\,dx=[x^2]_0^1=1$. Products may call for integration by parts; a composition with its derivative may call for substitution. The worked solutions show the actual choices.'),
('方程、初值、边界：三个信息缺一不可','Equation, initial data, boundary data',
'常微分方程的未知函数通常只有一个自变量，例如 $y(t)$。偏微分方程的未知函数有多个自变量，例如位置和时间对应的 $u(x,t)$。\n\n方程规定内部怎样变化。初值规定 $t=0$ 时是什么样。边界规定区域边缘怎样，例如固定端 $u(0,t)=0$，绝热端 $u_x(0,t)=0$。做题前把它们分三行抄好。',
'An ordinary differential equation usually has a function of one variable, such as $y(t)$. A partial differential equation has several, such as position and time in $u(x,t)$.\n\nThe equation governs the interior. Initial data describe $t=0$. Boundary data describe the edge: a fixed end may have $u(0,t)=0$, while an insulated end has $u_x(0,t)=0$. Copy these into three separate lines before solving.'),
('展开与模态：把复杂形状拆成简单形状','Series and modes: build a shape from simple pieces',
'傅里叶展开把函数拆成正弦、余弦的叠加。每个系数决定那一种形状要放多少。\n\n“正交”像互不干扰的方向：用积分投影，可以单独取出一个系数。“本征函数”是能满足方程和边界的基本形状；边界决定允许哪些形状，不能先猜一个再忽略边界。',
'A Fourier series builds a function from sine and cosine pieces. Each coefficient determines how much of that shape is present.\n\nOrthogonal shapes behave like independent directions: an integral projection extracts one coefficient. Eigenfunctions are basic shapes compatible with the equation and boundaries. Let the boundaries select them before determining the coefficients.'),
('每道题都走这四步','Use these four steps on every problem',
'1. **找目标**：未知的是函数、积分、系数，还是本征值？\n2. **找线索**：周期想到傅里叶级数；初值常微分方程可考虑拉普拉斯；闭合围道先找奇点；有限区域先看边界。\n3. **写第一行**：从“带我做”里只展开当前一步，自己补算。\n4. **检查**：代回方程、核对初边值、检查符号和量纲。算不通就标记待复习。',
'1. **Name the target**: a function, integral, coefficient, or eigenvalue?\n2. **Read the clues**: periodic data suggest a Fourier series; an initial-value ODE may suit Laplace transforms; a closed contour calls for locating singularities; a finite region calls for examining boundaries.\n3. **Write the first line**: use one guided step, then do its calculation yourself.\n4. **Check**: substitute into the equation, check the data, and inspect signs and dimensions. Mark difficulties for review.')]
ROWS.insert(2,('可导、解析、整函数：分别要检查多大范围', 'Differentiable, analytic, entire: how much of the plane?', '**某点可导**：只检查一个点的复导数是否存在，而且从不同方向靠近都要给同一个结果。\n\n**在区域内解析**：这个开区域里的每一点都可导。只找到一个可导点，还不能说在它附近解析。\n\n**整函数**：整个复平面都解析。比如 $z^2$ 是整函数；$1/z$ 在 $z\\ne0$ 处解析，却不是整函数，因为原点没有定义。\n\n做判定题时先写清题目问哪一层。若 C–R 条件只在孤立的一个点成立，它最多帮助你找到该点可导，不能得到一个解析区域。', '**Differentiable at a point**: a complex derivative exists there, with the same limit from every approach direction.\n\n**Analytic on a region**: the function is differentiable at every point of that open region. Finding one differentiable point does not establish analyticity nearby.\n\n**Entire**: analytic on the whole complex plane. For example, $z^2$ is entire. The function $1/z$ is analytic where $z\\ne0$, but is not entire because it is undefined at the origin.\n\nIdentify which level a question asks about. Cauchy–Riemann equations holding at just one isolated point can help establish pointwise differentiability, but do not produce an analytic region.'))
def build(page,heading,md,reader):
 for title,en,body,body_en in ROWS:reader.register(title,en);reader.register(body,body_en)
 h=heading('START SMALL','先会这几个符号，再开始做题','每次学一小段，马上用一道题验证。')
 for i,(title,en,body,body_en) in enumerate(ROWS):h+='<section class="card prose"><p class="eyebrow">'+str(i+1).zfill(2)+'</p><h2>'+reader.pair(title,en)+'</h2>'+md(body)+'</section>'
 z='小检查：若 $u=x^2+3y$，$u_x$ 与 $u_{xx}$ 分别是多少？';e='Quick check: for $u=x^2+3y$, what are $u_x$ and $u_{xx}$?';reader.register(z,e)
 a='$u_x=2x$，$u_{xx}=2$。对 $x$ 求导时，$3y$ 是常数，所以导数为0。';b='$u_x=2x$ and $u_{xx}=2$. When differentiating with respect to $x$, $3y$ is constant and its derivative is zero.';reader.register(a,b)
 h+='<section class="card"><h2>'+reader.pair('试一下，再往下走','Try this before moving on')+'</h2>'+md(z)+'<details class="reveal"><summary>'+reader.pair('展开检查','Open to check')+'</summary><div class="reveal-body">'+md(a)+'</div></details><a class="primary-btn" href="chapter-1.html">'+reader.pair('进入第一章','Open Chapter 1')+' →</a></section>'
 page('beginner.html','从这里开始',h,'beginner.html')
