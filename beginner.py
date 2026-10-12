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
('先分清方程、初值与边界','Distinguish the equation, initial data, and boundaries',
'常微分方程的未知函数通常只有一个自变量，例如 $y(t)$。偏微分方程的未知函数有多个自变量，例如位置和时间对应的 $u(x,t)$。\n\n方程规定内部怎样变化。初值规定 $t=0$ 时是什么样。边界规定区域边缘怎样，例如固定端 $u(0,t)=0$，绝热端 $u_x(0,t)=0$。做题前分别找出题目给了哪几类信息：稳态问题没有时间初值，整空间问题也没有有限端点。',
'An ordinary differential equation usually has a function of one variable, such as $y(t)$. A partial differential equation has several, such as position and time in $u(x,t)$.\n\nThe equation governs the interior. Initial data describe $t=0$. Boundary data describe the edge: a fixed end may have $u(0,t)=0$, while an insulated end has $u_x(0,t)=0$. Identify which types the problem supplies: a steady problem has no time initial data, and a whole-space problem has no finite endpoints.'),
('展开与模态：把复杂形状拆成简单形状','Series and modes: build a shape from simple pieces',
'傅里叶展开把函数拆成正弦、余弦的叠加。每个系数决定那一种形状要放多少。\n\n“正交”像互不干扰的方向：用积分投影，可以单独取出一个系数。“本征函数”是能满足方程和边界的基本形状；边界决定允许哪些形状，不能先猜一个再忽略边界。',
'A Fourier series builds a function from sine and cosine pieces. Each coefficient determines how much of that shape is present.\n\nOrthogonal shapes behave like independent directions: an integral projection extracts one coefficient. Eigenfunctions are basic shapes compatible with the equation and boundaries. Let the boundaries select them before determining the coefficients.'),
('每道题都走这四步','Use these four steps on every problem',
'1. **找目标**：未知的是函数、积分、系数，还是本征值？\n2. **找线索**：周期想到傅里叶级数；初值常微分方程可考虑拉普拉斯；闭合围道先找奇点；有限区域先看边界。\n3. **写第一行**：从“带我做”里只展开当前一步，自己补算。\n4. **检查**：代回方程、核对初边值、检查符号和量纲。算不通就标记待复习。',
'1. **Name the target**: a function, integral, coefficient, or eigenvalue?\n2. **Read the clues**: periodic data suggest a Fourier series; an initial-value ODE may suit Laplace transforms; a closed contour calls for locating singularities; a finite region calls for examining boundaries.\n3. **Write the first line**: use one guided step, then do its calculation yourself.\n4. **Check**: substitute into the equation, check the data, and inspect signs and dimensions. Mark difficulties for review.')]
ROWS.insert(2,('可导、解析、整函数：分别要检查多大范围', 'Differentiable, analytic, entire: how much of the plane?', '**某点可导**：只检查一个点的复导数是否存在，而且从不同方向靠近都要给同一个结果。\n\n**在区域内解析**：这个开区域里的每一点都可导。只找到一个可导点，还不能说在它附近解析。\n\n**整函数**：整个复平面都解析。比如 $z^2$ 是整函数；$1/z$ 在 $z\\ne0$ 处解析，却不是整函数，因为原点没有定义。\n\n做判定题时先写清题目问哪一层。若 C–R 条件只在孤立的一个点成立，它最多帮助你找到该点可导，不能得到一个解析区域。', '**Differentiable at a point**: a complex derivative exists there, with the same limit from every approach direction.\n\n**Analytic on a region**: the function is differentiable at every point of that open region. Finding one differentiable point does not establish analyticity nearby.\n\n**Entire**: analytic on the whole complex plane. For example, $z^2$ is entire. The function $1/z$ is analytic where $z\\ne0$, but is not entire because it is undefined at the origin.\n\nIdentify which level a question asks about. Cauchy–Riemann equations holding at just one isolated point can help establish pointwise differentiability, but do not produce an analytic region.'))
PRACTICE_KEYS=['parts','fractions','projection','lifting','recurrence','eigenvalues']
PRACTICE=[
('分部积分：具体怎样选两部分','Integration by parts: choosing the two pieces',
r'要算 $I=\int_0^\pi x\sin x\,dx$，把容易求导的 $x$ 选为 $u$，把容易积分的 $\sin x\,dx$ 选为 $dv$。于是 $du=dx$、$v=-\cos x$。'+'\n\n'+r'套用 $\int u\,dv=uv-\int v\,du$：$I=[-x\cos x]_0^\pi+\int_0^\pi\cos x\,dx=\pi+0=\pi$。别漏掉边界项，它常常就是傅里叶系数的来源。',
r'For $I=\int_0^\pi x\sin x\,dx$, choose the easy-to-differentiate factor $x$ as $u$ and the easy-to-integrate factor $\sin x\,dx$ as $dv$. Then $du=dx$ and $v=-\cos x$.'+'\n\n'+r'Apply $\int u\,dv=uv-\int v\,du$: $I=[-x\cos x]_0^\pi+\int_0^\pi\cos x\,dx=\pi+0=\pi$. Retain the boundary term; it often supplies the Fourier coefficient.',
r'换成 $\int_0^\pi x\cos x\,dx$，结果是多少？',r'What is $\int_0^\pi x\cos x\,dx$?',
r'取 $u=x$、$v=\sin x$，边界项为零；余下 $-\int_0^\pi\sin x\,dx=-2$。',r'Choose $u=x$, $v=\sin x$. The boundary term vanishes, leaving $-\int_0^\pi\sin x\,dx=-2$.','chapter-2.html#ex-2.1-4'),
('部分分式：把像函数拆成能查表的项','Partial fractions: split a transform into table entries',
r'例如 $Y(p)=1/[p(p+1)]$。先设 $Y=A/p+B/(p+1)$，乘去分母得 $1=A(p+1)+Bp$。代 $p=0$ 得 $A=1$；代 $p=-1$ 得 $B=-1$。'+'\n\n'+r'因此 $Y=1/p-1/(p+1)$，逆变换为 $y=1-e^{-t}$。若分母含 $p^2$，应同时写 $A/p+B/p^2$；二重因子对应的 $1/p^2$ 还原为 $t$。',
r'For $Y(p)=1/[p(p+1)]$, set $Y=A/p+B/(p+1)$. Clear denominators to get $1=A(p+1)+Bp$. Setting $p=0$ gives $A=1$; setting $p=-1$ gives $B=-1$.'+'\n\n'+r'Thus $Y=1/p-1/(p+1)$ and $y=1-e^{-t}$. If the denominator contains $p^2$, include both $A/p+B/p^2$; the double-factor term $1/p^2$ inverts to $t$.',
r'$1/(p-2)^2$ 的原函数是什么？',r'What is the original function for $1/(p-2)^2$?',
r'$te^{2t}$。先记 $1/p^2\mapsto t$，再用指数平移。',r'$te^{2t}$. Start with $1/p^2\mapsto t$, then apply the exponential shift.','chapter-2.html#ex-2.4-5'),
('正交投影：为什么乘一下、积一下就能取系数','Orthogonal projection: why one integral extracts a coefficient',
r'设 $f(x)=3\sin x+2\sin2x$，区间为 $[0,\pi]$。两边乘 $\sin x$ 后积分，混合项 $\int_0^\pi\sin x\sin2x\,dx=0$，只剩 $\int_0^\pi f\sin x\,dx=3\pi/2$。'+'\n\n'+r'再除以所选基函数的平方积分 $\int_0^\pi\sin^2x\,dx=\pi/2$，便得到系数 $3$。一般写成“系数＝与该形状的乘积积分／该形状的平方积分”。这也解释了为什么公式里常有 $2/\pi$ 或 $2/l$。',
r'Let $f(x)=3\sin x+2\sin2x$ on $[0,\pi]$. Multiply by $\sin x$ and integrate. The mixed term $\int_0^\pi\sin x\sin2x\,dx=0$, leaving $\int_0^\pi f\sin x\,dx=3\pi/2$.'+'\n\n'+r'Divide by the basis squared integral $\int_0^\pi\sin^2x\,dx=\pi/2$ to obtain coefficient $3$. In general: coefficient = product integral with the chosen shape / squared integral of that shape. This explains factors such as $2/\pi$ or $2/l$.',
r'若 $f(x)=4\sin3x$，第二和第三个正弦系数分别是多少？',r'If $f(x)=4\sin3x$, what are its second and third sine coefficients?',
r'$b_2=0$、$b_3=4$。不同频率相互正交，第三个形状只投影到自身。',r'$b_2=0$ and $b_3=4$. Different frequencies are orthogonal; the third shape projects only onto itself.','chapter-3.html#ex-3.1-1'),
('边界齐次化：先减去一个满足端点的简单函数','Homogenizing boundaries: subtract a simple endpoint match',
r'若杆的端点一直保持 $u(0,t)=0$、$u(l,t)=10$，不能直接用两端为零的正弦级数表示整个 $u$。先选直线 $w(x)=10x/l$，它恰好满足这两个端点。'+'\n\n'+r'令 $v=u-w$，则 $v(0,t)=v(l,t)=0$，可以展开 $v$。初值也要同时减：$v(x,0)=u(x,0)-10x/l$。此处 $w$ 不随时间变化且 $w_{xx}=0$，所以不会给热方程添加新源项。',
r'If a rod has fixed endpoint temperatures $u(0,t)=0$ and $u(l,t)=10$, a sine series vanishing at both ends cannot represent all of $u$. Choose the line $w(x)=10x/l$ to match the endpoints first.'+'\n\n'+r'Let $v=u-w$, so $v(0,t)=v(l,t)=0$ and expand $v$. Shift the initial data too: $v(x,0)=u(x,0)-10x/l$. Here $w$ is time independent and $w_{xx}=0$, so it adds no source to the heat equation.',
r'若端点改为 $u(0,t)=5$、$u(l,t)=15$，可选哪条直线？',r'If the endpoints are $u(0,t)=5$ and $u(l,t)=15$, which line works?',
r'$w(x)=5+10x/l$；先代入两端检查，再令 $v=u-w$。',r'$w(x)=5+10x/l$. Check both endpoints first, then set $v=u-w$.','chapter-3.html#ex-3.2-1'),
('级数递推：先把幂次对齐','Series recurrences: align powers first',
r'以 $y^{\prime}=y$、$y(0)=1$ 为例。写 $y=\sum_{n=0}^\infty a_nx^n$。求导后重新编号，使同一行都是 $x^n$：$y^{\prime}=\sum_{n=0}^\infty(n+1)a_{n+1}x^n$。'+'\n\n'+r'比较每个幂次，得 $(n+1)a_{n+1}=a_n$。从 $a_0=1$ 依次算出 $a_1=1$、$a_2=1/2$。遇到二阶方程通常会有两条递推链，分别从常数项和一次项起步。',
r'For $y^{\prime}=y$ with $y(0)=1$, write $y=\sum_{n=0}^\infty a_nx^n$. Differentiate and reindex so every term uses $x^n$: $y^{\prime}=\sum_{n=0}^\infty(n+1)a_{n+1}x^n$.'+'\n\n'+r'Compare coefficients to get $(n+1)a_{n+1}=a_n$. Starting at $a_0=1$ gives $a_1=1$ and $a_2=1/2$. A second-order equation often has two recurrence chains, starting from the constant and linear terms.',
r'继续这条递推，$a_3$ 是多少？',r'Continue the recurrence: what is $a_3$?',
r'$a_3=a_2/3=1/6$。下标与分母都要向前推进一步。',r'$a_3=a_2/3=1/6$. Advance both the subscript and denominator by one step.','chapter-4.html#ex-4.2-1'),
('边界选本征值：先选形状，再定允许的频率','Boundary eigenvalues: choose the shape, then the frequency',
r'以 $X^{\prime\prime}+k^2X=0$、$X(0)=X(l)=0$ 为例。先讨论 $k>0$，通解为 $A\cos(kx)+B\sin(kx)$；左端让 $A=0$，右端要求 $B\sin(kl)=0$。'+'\n\n'+r'我们寻找非零形状，所以不能只取 $B=0$；必须令 $\sin(kl)=0$，得到 $k=n\pi/l$、$n\ge1$。圆柱问题只是把正弦换成 Bessel 函数：边界仍负责挑选函数的零点。零频情况要另外检查，不能靠除以 $k$ 的公式判断。',
r'For $X^{\prime\prime}+k^2X=0$ with $X(0)=X(l)=0$, for $k>0$ the general solution is $A\cos(kx)+B\sin(kx)$. The left endpoint gives $A=0$; the right requires $B\sin(kl)=0$.'+'\n\n'+r'We seek a nonzero shape, so simply taking $B=0$ is insufficient. Require $\sin(kl)=0$, giving $k=n\pi/l$, $n\ge1$. Cylinder problems replace sine by Bessel functions; the boundary still selects zeros. Check zero frequency separately rather than using a formula divided by $k$.',
r'若改成 $X^{\prime}(0)=0$、$X(l)=0$，正频率变成什么？',r'With $X^{\prime}(0)=0$ and $X(l)=0$, what are the positive frequencies?',
r'$k=(n+1/2)\pi/l$，$n\ge0$。左端留下余弦，右端要求余弦为零。',r'$k=(n+1/2)\pi/l$, $n\ge0$. The left condition selects cosine; the right sets cosine to zero.','chapter-5.html#ex-5.3-1')]
def build(page,heading,md,reader):
 for title,en,body,body_en in ROWS:reader.register(title,en);reader.register(body,body_en)
 h=heading('START SMALL','先会这几个符号，再开始做题','每次学一小段，马上用一道题验证。')
 for i,(title,en,body,body_en) in enumerate(ROWS):h+='<section class="card prose"><p class="eyebrow">'+str(i+1).zfill(2)+'</p><h2>'+reader.pair(title,en)+'</h2>'+md(body)+'</section>'
 h+='<section class="card prose"><h2>'+reader.pair('卡在某一步？只练对应这一项','Stuck on one step? Practice just that skill')+'</h2><p>'+reader.pair('下面六项可以按需阅读，不必一次看完。先做小检查，再回到原题。','Use these six skills as needed. Try the quick check, then return to your problem.')+'</p></section>'
 for key,(title,en,body,body_en,q,qe,a,ae,link) in zip(PRACTICE_KEYS,PRACTICE):
  for z,e in [(body,body_en),(q,qe),(a,ae)]:reader.register(z,e)
  h+='<section class="card prose" id="skill-'+key+'"><h2>'+reader.pair(title,en)+'</h2>'+md(body)+'<strong>'+reader.pair('自己试一下','Try it yourself')+'</strong>'+md(q)+'<details class="reveal"><summary>'+reader.pair('展开检查','Open to check')+'</summary><div class="reveal-body">'+md(a)+'</div></details><p><a href="'+link+'">'+reader.pair('回到这类题','Use this in a problem')+' →</a></p></section>'
 z='小检查：若 $u=x^2+3y$，$u_x$ 与 $u_{xx}$ 分别是多少？';e='Quick check: for $u=x^2+3y$, what are $u_x$ and $u_{xx}$?';reader.register(z,e)
 a='$u_x=2x$，$u_{xx}=2$。对 $x$ 求导时，$3y$ 是常数，所以导数为0。';b='$u_x=2x$ and $u_{xx}=2$. When differentiating with respect to $x$, $3y$ is constant and its derivative is zero.';reader.register(a,b)
 h+='<section class="card"><h2>'+reader.pair('试一下，再往下走','Try this before moving on')+'</h2>'+md(z)+'<details class="reveal"><summary>'+reader.pair('展开检查','Open to check')+'</summary><div class="reveal-body">'+md(a)+'</div></details><a class="primary-btn" href="chapter-1.html">'+reader.pair('进入第一章','Open Chapter 1')+' →</a></section>'
 page('beginner.html','从这里开始',h,'beginner.html')
