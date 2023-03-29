# c++反汇编(x86)


## 1.类型大小

### 1. 基本数据类型

```c++
printf("%d\n", sizeof(char));		//1
printf("%d\n", sizeof(short int));	//2
printf("%d\n", sizeof(int));		//4
printf("%d\n", sizeof(long int));	//4
printf("%d\n", sizeof(__int64));	//8
printf("%d\n", sizeof(float));		//4
printf("%d\n", sizeof(double));		//8
```

### 2. 数组类型

```c++
char arr1[10] = { 0 };
short arr2[10] = { 0 };
int arr3[10] = { 0 };

printf("%d\n", sizeof(arr1));	//10
printf("%d\n", sizeof(arr2));	//20
printf("%d\n", sizeof(arr3));	//40

printf("%d\n", sizeof(arr1[10]));  //sizeof(char)	1
printf("%d\n", sizeof(arr2[10]));  //sizeof(short)	2
printf("%d\n", sizeof(arr3[10]));  //sizeof(int)	4
```

### 3. 数据对齐

1. 为什么要有数据对齐？

本质：效率还是空间，二选一的结果；

`#pragma pack`的基本用法为：

```md 
#pragma pack( n )
结构体...
#pragma pack(  )
```

对齐参数：n为字节对齐数，其取值为1、2、4、8，默认是8。如果这个值比结构体成员的sizeof值小，那么该成员的偏移量应该以此值为准，
即是说，结构体成员的偏移量应该取二者的最小值.

2. 结构对齐大小

如果这个值比结构体成员的sizeof值小，那么该成员的偏移量应该以此值为准，即是说，结构体成员的偏移量应该取二者的最小值；

对齐原则：

* 原则一：数据成员对齐规则：结构的数据成员，第一个数据成员放在offset为0的地方，以后每个数据成员存储的起始位置要从该成员大小的整数倍开始(比如int在32位机为４字节，则要从4的整数倍地址开始存储).

* 原则二：结构体的总大小，也就是sizeof的结果，必须是其内部最大成员的整数倍，不足的要补齐。

* 原则三：如果一个结构里有某些结构体成员，则结构体成员要从其内部最大元素大小的整数倍地址开始存储。

	> (struct a里存有struct b，b里有char，int，double等元素，那b应该从8的整数倍开始存储.)

原则四：对齐参数如果比结构体成员的sizeof值小，该成员的偏移量应该以此值为准.也就是说，结构体成员的偏移量应该取二者的最小值

3. 建议：

按照数据类型由小到大的顺序进行书写  

4. 实例

```c++
//16
struct S1
{
	char c;   //8
	double i; //8
};

//40
struct S2
{
	char c1;  //8
	S1 s;     //16 => char c; double i;
	char c2;  //8
	double c3;  //8
};

//32
struct S3
{
	char c1;  //8
	S1 s;     //16 => char c; double i;
	char c2;  // => sizeof(c2) + sizeof(c3) = 2 + 6 = 8
	char c3;
};

//12
struct S4
{
	int c1;     //sizeof(int) + sizeof(char) * 5 =》 4 + 4 + 1 + 3(填充) = 12
	char c2[5];
};

//16
struct S5
{
	int c1;     //sizeof(int) + sizeof(char) * 10 =》 4 + (4 * 2 + 2 + 2(填充)) = 16
	char c2[10];
};

int main() {
	int a = sizeof(S1);
	int b = sizeof(S2);
	int c = sizeof(S3);
	int d = sizeof(S4);
	int e = sizeof(S5);

	return 0;
}
```

## 2. 面向对象

### 2.1 对象

1. 绕过编译器，修改对象的私有成员：

```c++
#include <iostream>

class Test {
public:
	Test(int x, int y) {
		this->x = x;
		this->y = y;
	}

	void pri() {
		std::cout << "x : " << x << "\ny : " << y << std::endl;;
	}

private:
	int x;
	int y;
};

int main() {

	Test t(1, 2);

	int* p = (int*)&t;

	int n = *p;
	int m = *(p + 1);

	*p = 3;
	*(p + 1) = 4;

	std::cout << "n : " << n << "\nm : " << m << std::endl;;

	t.pri();

	system("pause");

	return 0;
}
```

2. 绕过编译器，调用对象的私有成员函数：

```c++
#include <iostream>

struct Base
{
private:
	virtual void Function_1()
	{
		printf("Base:Function_1...\n");
	}
	virtual void Function_2()
	{
		printf("Base:Function_2...\n");
	}
	virtual void Function_3()
	{
		printf("Base:Function_3...\n");
	}
};

int main() {

	Base b;
	Base* ptr = &b;

	void(*f1)(void) = (void(*)(void))(*((int*)(*(int*)&b + 0)));
	void(*f2)(void) = (void(*)(void))(*((int*)(*(int*)&b + 4)));
	void(*f3)(void) = (void(*)(void))(*((int*)(*(int*)&b + 8)));

	/*
	0. 函数指针：(void(*)(void))
	1. 指向虚表的地址：(*(int *)&b)
	2. 虚函数的地址(或第一个虚函数的地址)：(*((int*)(*(int *)&b + 0)))
	*/

	f1();
	f2();
	f3();

	system("pause");

	return 0;
}
```

总结：

* private修饰的成员与普通的成员没有区别 只是编译器会检测。
* private修饰的成员只有自己的其他成员才能访问；

3. struct 与 class

* 编译器默认class中的成员为private，而struct中的成员为public
* class 默认private继承，struct 默认public继承

4. 指针与引用

```c++
#include <iostream>

int main() {
	int a = 12;

	int* ptr = &a;
	int& ref = a;

	system("pause");

	return 0;
}
```

```c++
	int a = 12;
008F1728  mov         dword ptr [ebp-0Ch],0Ch  

	int* ptr = &a;
008F172F  lea         eax,[ebp-0Ch]  
008F1732  mov         dword ptr [ebp-18h],eax  
	int& ref = a;
008F1735  lea         eax,[ebp-0Ch]  
008F1738  mov         dword ptr [ebp-24h],eax  
```

总结：指针与引用在汇编层次，没有任何区别；

## 2.2 虚表

继承

* 父类中的私有成员是会被继承的
* 只是编译器不允许直接进行访问

1. 当类中有虚函数时，会多一个属性，4个字节(单一继承)
2. 多出的属性是一个地址，指向一张表，里面存储了所有虚函数的地址

> 在x86中，指针类型大小都为4个字节

### 2.2.1 非继承虚函数表

```c++
//普通继承，非覆盖
struct Base
{
public:
	virtual void Function_1()
	{
		printf("Base:Function_1...\n");
	}
	virtual void Function_2()
	{
		printf("Base:Function_2...\n");
	}
	virtual void Function_3()
	{
		printf("Base:Function_3...\n");
	}
};

int main() {
	Base base;
	Base* ptr = &base;
	
	//断点到此处
	ptr->Function_1();
	ptr->Function_2();
	ptr->Function_3();

	system("pause");

	return 0;
}
```

汇编如下:

```c++
	Base base;
009D51D8  lea         ecx,[ebp-0Ch]  
009D51DB  call        009D103C  
	Base* ptr = &base;
009D51E0  lea         eax,[ebp-0Ch] ;获得base的地址 
009D51E3  mov         dword ptr [ebp-18h],eax 
	
	//断点到此处
	ptr->Function_1();
009D51E6  mov         eax,dword ptr [ebp-18h]  ;&base
009D51E9  mov         edx,dword ptr [eax]  ;base的虚表地址
009D51EB  mov         esi,esp  
009D51ED  mov         ecx,dword ptr [ebp-18h]  
009D51F0  mov         eax,dword ptr [edx]  ;第一个函数的地址
009D51F2  call        eax  
009D51F4  cmp         esi,esp  
009D51F6  call        009D1140  
	ptr->Function_2();
009D51FB  mov         eax,dword ptr [ebp-18h]  
009D51FE  mov         edx,dword ptr [eax]  
009D5200  mov         esi,esp  
009D5202  mov         ecx,dword ptr [ebp-18h]  
009D5205  mov         eax,dword ptr [edx+4]  ;第二个函数的地址，偏移4个字节
009D5208  call        eax  
009D520A  cmp         esi,esp  
009D520C  call        009D1140  
	ptr->Function_3();
009D5211  mov         eax,dword ptr [ebp-18h]  
009D5214  mov         edx,dword ptr [eax]  
009D5216  mov         esi,esp  
009D5218  mov         ecx,dword ptr [ebp-18h]  
009D521B  mov         eax,dword ptr [edx+8]  ;第三个函数的地址，偏移8个字节
009D521E  call        eax  
009D5220  cmp         esi,esp  
009D5222  call        009D1140  
```

验证：

```c++
void TestMethod()
{
	//查看 Sub 的虚函数表          
	Base base;
	Base* ptr = &base;  //包含一个虚表指针

	printf("base 的地址为：%x\n", &base);
	//对象的前四个字节就是虚函数表         
	printf("base 的虚函数表地址为：%x\n", *(int*)&base);
	for (int i = 0; i < 3; i++) {
		printf("虚函数%d的地址：%x\n", i + 1, *((int*)(*(int*)&base) + i));
	}

	//通过函数指针调用函数，验证正确性        
	typedef void(*pFunction)(void);
	pFunction pFn;

	for (int i = 0; i < 3; i++)
	{
		int temp = *((int*)(*(int*)&base) + i);
		pFn = (pFunction)temp;
		pFn();
	}
}
```

### 2.2.2 继承非覆盖虚函数表

父类的虚函数表和子类不相同，**每个类都独有自己的一份虚函数表；**

通过调试不难发现，Sub子类的的虚表就是：Function_1、Function_2、Function_3、Function_4、Function_5、Function_6 这个6个函数的地址；Base基类的虚表就是：Function_1、Function_2、Function_3 这个3个函数地址；

```c++
#include <iostream>

//普通继承，非覆盖
struct Base
{
public:
	virtual void Function_1()
	{
		printf("Base:Function_1...\n");
	}
	virtual void Function_2()
	{
		printf("Base:Function_2...\n");
	}
	virtual void Function_3()
	{
		printf("Base:Function_3...\n");
	}
};
struct Sub :Base
{
public:
	virtual void Function_4()
	{
		printf("Sub:Function_4...\n");
	}
	virtual void Function_5()
	{
		printf("Sub:Function_5...\n");
	}
	virtual void Function_6()
	{
		printf("Sub:Function_6...\n");
	}
};

void TestMethod() {
	//查看 Sub， Base 的虚函数表        
	Sub sub;
	Base base;

	Base* ptr1 = &sub;  //包含一个虚表指针
	Base* ptr2 = &base;

	printf("base 的地址为：%x\n", &base);
	//对象的前四个字节就是虚函数表         
	printf("base 的虚函数表地址为：%x\n", *(int*)&base);
	for (int i = 0; i < 3; i++) {
		printf("Base虚函数%d的地址：%x\n", i + 1, *((int*)(*(int*)&base) + i));
	}
	//通过函数指针调用函数，验证正确性        
	typedef void(*pFunction)(void);
	pFunction p1Fn;

	for (int i = 0; i < 3; i++)
	{
		int temp = *((int*)(*(int*)&base) + i);
		p1Fn = (pFunction)temp;
		p1Fn();
	}

	std::cout << std::endl;

	printf("Sub 的地址为：%x\n", &sub);
	//对象的前四个字节就是虚函数表         
	printf("Sub 的虚函数表地址为：%x\n", *(int*)&sub);
	for (int i = 0; i < 6; i++) {
		printf("Sub虚函数%d的地址：%x\n", i + 1, *((int*)(*(int*)&sub) + i));
	}
	//通过函数指针调用函数，验证正确性        
	pFunction p2Fn;
	for (int i = 0; i < 6; i++)
	{
		int temp = *((int*)(*(int*)&sub) + i);
		p2Fn = (pFunction)temp;
		p2Fn();
	}
}

int main() {

	TestMethod();

	system("pause");

	return 0;
}
```

### 2.2.3 继承覆盖虚函数表

子类优先按照基类声明的顺序添加虚函数；

```c++
#include <iostream>

//普通继承，覆盖
struct Base
{
public:
	virtual void Function_1()
	{
		printf("Base:Function_1...\n");
	}
	virtual void Function_2()
	{
		printf("Base:Function_2...\n");
	}
	virtual void Function_3()
	{
		printf("Base:Function_3...\n");
	}
};
struct Sub :Base
{
public:
	virtual void Function_1()
	{
		printf("Sub:Function_1...\n");
	}
	virtual void Function_5()
	{
		printf("Sub:Function_5...\n");
	}
	virtual void Function_3()
	{
		printf("Sub:Function_3...\n");
	}
};


//查看 Sub， Base 的虚函数表
void TestMethod()
{
	//查看 Sub， Base 的虚函数表        
	Sub sub;
	Base base;

	Base* ptr1 = &sub;  //包含一个虚表指针
	Base* ptr2 = &base;

	printf("base 的地址为：%x\n", &base);
	//对象的前四个字节就是虚函数表         
	printf("base 的虚函数表地址为：%x\n", *(int*)&base);
	for (int i = 0; i < 3; i++) {
		printf("Base虚函数%d的地址：%x\n", i + 1, *((int*)(*(int*)&base) + i));
	}
	//通过函数指针调用函数，验证正确性        
	typedef void(*pFunction)(void);
	pFunction p1Fn;

	for (int i = 0; i < 3; i++)
	{
		int temp = *((int*)(*(int*)&base) + i);
		p1Fn = (pFunction)temp;
		p1Fn();
	}

	std::cout << std::endl;

	printf("Sub 的地址为：%x\n", &sub);
	//对象的前四个字节就是虚函数表         
	printf("Sub 的虚函数表地址为：%x\n", *(int*)&sub);
	for (int i = 0; i < 4; i++) {
		printf("Sub虚函数%d的地址：%x\n", i + 1, *((int*)(*(int*)&sub) + i));
	}

	//通过函数指针调用函数，验证正确性        
	pFunction p2Fn;
	for (int i = 0; i < 4; i++)
	{
		int temp = *((int*)(*(int*)&sub) + i);
		p2Fn = (pFunction)temp;
		p2Fn();
	}
}

int main() {

	TestMethod();

	system("pause");

	return 0;
}
```

### 2.2.4 多继承非覆盖虚函数表

```c++
#include <iostream>

struct Base1
{
public:
	virtual void Fn_1()
	{
		printf("Base1:Fn_1...\n");
	}
	virtual void Fn_2()
	{
		printf("Base1:Fn_2...\n");
	}
};
struct Base2
{
public:
	virtual void Fn_3()
	{
		printf("Base2:Fn_3...\n");
	}
	virtual void Fn_4()
	{
		printf("Base2:Fn_4...\n");
	}
};
struct Sub :Base1, Base2
{
public:
	virtual void Fn_5()
	{
		printf("Sub:Fn_5...\n");
	}
	virtual void Fn_6()
	{
		printf("Sub:Fn_6...\n");
	}
};

int main() {
	//查看 Sub 的虚函数表                 
	Sub sub;

	//通过函数指针调用函数，验证正确性               
	typedef void(*pFunction)(void);

	//对象的前四个字节是第一个虚表: 经过编译器优化：Base1 + Sub 的虚函数组成的表                 
	printf("Sub的第一个虚表的虚函数表地址为：%x\n", *(int*)&sub);
	pFunction pFn;
	for (int i = 0; i < 4; i++)
	{
		int temp = *((int*)(*(int*)&sub) + i);
		if (temp == 0)
		{
			break;
		}
		pFn = (pFunction)temp;
		pFn();
	}

	//对象的第二个四字节是第二个虚表, 根据编译器的优化 =》 Base2的虚表               
	printf("Sub的第二个虚表的虚函数表地址为：%x\n", *(int*)((int*)&sub + 4));
	pFunction pFn1;
	for (int k = 0; k < 2; k++)
	{
		int temp = *((int*)(*(int*)((int)&sub + 4)) + k);
		pFn1 = (pFunction)temp;
		pFn1();
	}

	system("pause");

	return 0;
}
```

结论：Sub的虚表由两个虚表组成：

1. Base1 + Sub 的虚函数组成的虚表;
2. Base2组成的虚表

>猜测：之后的继承的每个类有单独的虚表，如Base2一样；

### 2.2.5 多继承覆盖虚函数表

```c++
#include <iostream>

struct Base1
{
public:
	virtual void Fn_1()
	{
		printf("Base1:Fn_1...\n");
	}
	virtual void Fn_2()
	{
		printf("Base1:Fn_2...\n");
	}
};
struct Base2
{
public:
	virtual void Fn_3()
	{
		printf("Base2:Fn_3...\n");
	}
	virtual void Fn_4()
	{
		printf("Base2:Fn_4...\n");
	}
};

struct Base3
{
public:
	virtual void Fn_6()
	{
		printf("Base3:Fn_6...\n");
	}
	virtual void Fn_7()
	{
		printf("Base3:Fn_7...\n");
	}
};

struct Sub :Base1, Base2, Base3
{
public:
	virtual void Fn_1()
	{
		printf("Sub:Fn_1...\n");
	}
	virtual void Fn_3()
	{
		printf("Sub:Fn_3...\n");
	}
	virtual void Fn_5()
	{
		printf("Sub:Fn_5...\n");
	}

	virtual void Fn_6()
	{
		printf("Sub:Fn_6...\n");
	}

	virtual void Fn_8()
	{
		printf("Sub:Fn_8...\n");
	}
};


int main() {
	//查看 Sub 的虚函数表                 
	Sub sub;

	//通过函数指针调用函数，验证正确性               
	typedef void(*pFunction)(void);

	//对象的前四个字节是第一个虚表: 经过编译器优化：Base1 + Sub 的虚函数组成的表                
	printf("第一个虚表 的虚函数表地址为：%x\n", *(int*)&sub);
	pFunction pFn;
	for (int i = 0; i < 4; i++)
	{
		int temp = *((int*)(*(int*)&sub) + i);
		if (temp == 0)
		{
			break;
		}
		pFn = (pFunction)temp;
		pFn();
	}

	//对象的第二个四字节是第二个虚表, 根据编译器的优化 =》 Base2的虚表             
	printf("第二个虚表 的虚函数表地址为：%x\n", *(int*)((int)&sub + 4));
	pFunction pFn1;
	for (int k = 0; k < 2; k++)
	{
		int temp = *((int*)(*(int*)((int)&sub + 4)) + k);
		pFn1 = (pFunction)temp;
		pFn1();
	}

	//对象的第三个四字节是第三个虚表, 根据编译器的优化 =》 Base3的虚表             
	printf("第三个虚表 的虚函数表地址为：%x\n", *(int*)((int)&sub + 8));
	for (int k = 0; k < 2; k++)
	{
		int temp = *((int*)(*(int*)((int)&sub + 8)) + k);
		pFn1 = (pFunction)temp;
		pFn1();
	}

	system("pause");

	return 0;
}
```

结论：Sub的虚表由三个虚表组成，按照继承顺序组合：

1. Base1 + Sub 的虚函数组成的虚表：Sub::Fn_1(), Base1::Fn_2(), Sub::Fn_5(), Sub::Fn_8();
2. Base2 + Sub 的虚函数组成的虚表：Sub::Fn_3(), Base2::Fn_4();
3. Base3 + Sub 的虚函数组成的虚表：Sub::Fn_6(), Base3::Fn_7();

### 2.2.6 单一连续继承，无函数覆盖

```c++
#include <iostream>

struct Base1
{
public:
	virtual void Fn_1()
	{
		printf("Base1:Fn_1...\n");
	}
	virtual void Fn_2()
	{
		printf("Base1:Fn_2...\n");
	}
};
struct Base2 :Base1
{
public:
	virtual void Fn_3()
	{
		printf("Base2:Fn_3...\n");
	}
	virtual void Fn_4()
	{
		printf("Base2:Fn_4...\n");
	}
};
struct Sub :Base2
{
public:
	virtual void Fn_5()
	{
		printf("Sub:Fn_5...\n");
	}
	virtual void Fn_6()
	{
		printf("Sub:Fn_6...\n");
	}
};
int main(int argc, char* argv[])
{
	//查看 Sub 的虚函数表            
	Sub sub;

	//观察大小：虚函数表只有一个           
	printf("%x\n", sizeof(sub));

	//通过函数指针调用函数，验证正确性          
	typedef void(*pFunction)(void);


	//对象的前四个字节是就是虚函数表            
	printf("Sub 的虚函数表地址为：%x\n", *(int*)&sub);

	pFunction pFn;

	for (int i = 0; i < 6; i++)
	{
		int temp = *((int*)(*(int*)&sub) + i);
		if (temp == 0)
		{
			break;
		}
		pFn = (pFunction)temp;
		pFn();
	}

	return 0;
}
```

结论：单一继承，虚表只有一个；

### 2.2.7 单一连续继承，有函数覆盖

```c++
#include <iostream>

struct Base1
{
public:
	virtual void Fn_1()
	{
		printf("Base1:Fn_1...\n");
	}
	virtual void Fn_2()
	{
		printf("Base1:Fn_2...\n");
	}
};
struct Base2 :Base1
{
public:
	virtual void Fn_1()
	{
		printf("Base2:Fn_1...\n");
	}
	virtual void Fn_3()
	{
		printf("Base2:Fn_3...\n");
	}
};
struct Sub :Base2
{
public:
	virtual void Fn_1()
	{
		printf("Sub:Fn_1...\n");
	}

	virtual void Fn_5()
	{
		printf("Sub:Fn_5...\n");
	}
};
int main(int argc, char* argv[])
{
	//查看 Sub 的虚函数表            
	Sub sub;

	//观察大小：虚函数表只有一个           
	printf("%x\n", sizeof(sub));

	//通过函数指针调用函数，验证正确性          
	typedef void(*pFunction)(void);


	//对象的前四个字节是就是虚函数表            
	printf("Sub 的虚函数表地址为：%x\n", *(int*)&sub);

	pFunction pFn;

	for (int i = 0; i < 6; i++)
	{
		int temp = *((int*)(*(int*)&sub) + i);
		if (temp == 0)
		{
			break;
		}
		pFn = (pFunction)temp;
		pFn();
	}

	return 0;
}
```
结论：单一继承，虚表只有一个；

### 2.2.8 例子

1. 定义一个父类：Base 有两个成员X,Y 有一个函数Print(非virtul)  
能够打印X,Y的值。

```c++
#include <iostream>

class Base {
public:
	Base(int x, int y) : x(x), y(y) {
	};

private:
	int x, y;

};

void prt(void* ptr) {
	printf("X: %d Y: %d\n", *((int*)ptr), *((int*)ptr + 1));
}

int main() {

	Base base(1, 2);

	prt(&base);

	system("pause");

	return 0;
}
```

2. 定义3个子类：Sub1有一个成员A, Sub2有一个成员B, Sub3  有一个成员C; 每个子类有一个函数Print(非virtul)，打印所有成员。

* Sub1:打印X Y A
* Sub2:打印X Y B
* Sub3:打印X Y C

```c++
#include <iostream>

class Base {
public:
	Base(int x, int y) : x(x), y(y) {
	};

private:
	int x, y;
};

class  Sub1 : public Base {
public:
	Sub1(int x, int y, int n) : Base(x, y), a(n) {
	}

	void prt(void* ptr) {
		printf("X: %d Y: %d #: %d\n", *((int*)ptr), *((int*)ptr + 1), *((int*)ptr + 2));
	}

private:
	int a;
};

class  Sub2 : public Base {
public:
	Sub2(int x, int y, int n) : Base(x, y), b(n) {
	}

	void prt(void* ptr) {
		printf("X: %d Y: %d #: %d\n", *((int*)ptr), *((int*)ptr + 1), *((int*)ptr + 2));
	}

private:
	int b;
};

class  Sub3 : public Base {
public:
	Sub3(int x, int y, int n) : Base(x, y), c(n) {
	}

	void prt(void* ptr) {
		printf("X: %d Y: %d #: %d\n", *((int*)ptr), *((int*)ptr + 1), *((int*)ptr + 2));
	}

private:
	int c;
};

int main() {

	Sub1 sub1(1, 2, 3);
	Sub1 sub2(4, 5, 6);
	Sub1 sub3(7, 8, 9);

	sub1.prt(&sub1);
	sub2.prt(&sub2);
	sub3.prt(&sub3);

	system("pause");

	return 0;
}
```

总结：子类的成员 = 基类的成员 + 子类的成员

3. 将上面所有的Print函数改成virtul 继续观察效果. 

```c++
#include <iostream>

class Base {
public:
	Base(int x, int y) : x(x), y(y) {
	};

private:
	int x, y;

};

class  Sub1 : public Base {
public:
	Sub1(int x, int y, int n) : Base(x, y), a(n) {
	}

	virtual void prt(void* ptr) {
		printf("X: %d Y: %d #: %d\n", *((int*)ptr + 1), *((int*)ptr + 2), *((int*)ptr + 3));
	}

private:
	int a;
};

class  Sub2 : public Base {
public:
	Sub2(int x, int y, int n) : Base(x, y), b(n) {
	}

	virtual void prt(void* ptr) {
		printf("X: %d Y: %d #: %d\n", *((int*)ptr + 1), *((int*)ptr + 2), *((int*)ptr + 3));
	}

private:
	int b;
};

class  Sub3 : public Base {
public:
	Sub3(int x, int y, int n) : Base(x, y), c(n) {
	}

	virtual void prt(void* ptr) {
		printf("X: %d Y: %d #: %d\n", *((int*)ptr + 1), *((int*)ptr + 2), *((int*)ptr + 3));
	}

private:
	int c;
};

int main() {

	Sub1 sub1(1, 2, 3);
	Sub1 sub2(4, 5, 6);
	Sub1 sub3(7, 8, 9);

	sub1.prt(&sub1);
	sub2.prt(&sub2);
	sub3.prt(&sub3);

	system("pause");

	return 0;
}
```

总结：子类成员在对象的前4字节(虚表地址)之后，子类的成员 = 基类的成员 + 子类的成员



---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/c++%E5%8F%8D%E6%B1%87%E7%BC%96/  

