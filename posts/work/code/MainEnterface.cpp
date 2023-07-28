#include "stdafx.h"
#include "MainEnterface.h"
#include "Version.h"
#include "Instance.cpp"
#include "Define.h"
#include "NetInstance.h"
#include "MyFile.h"
#include <vector>
#include <map>
#include <string>
#include <sstream>
#include <windows.h>
#include <set>
#include <iomanip>
#include <openssl/sha.h>

//CString PATH = CRunTime::GetInstance()->GetExePath() + "File\\GM\\";
//CString PATH = CRunTime::GetInstance()->GetExePath() + "File\\GmChina\\";
//CString PATH = CRunTime::GetInstance()->GetExePath() + "File\\GmChina_old\\";
//CString PATH = CRunTime::GetInstance()->GetExePath() + "File\\Conqueror_old\\";
CString PATH = CRunTime::GetInstance()->GetExePath() + "File\\Conqueror_en\\";
D_BOOL isCN = false;
CString	ptr_ = "Conqueror_";

static unsigned int names_cnt = 1;

CString PATH_Menu = CRunTime::GetInstance()->GetExePath() + "File\\excel\\" + (isCN ? "Menus_cn.bin" : "Menus_en.bin");
CString PATH_MenuHead = CRunTime::GetInstance()->GetExePath() + "File\\MenuHead.bin";
CString PATH_ECUMenu = CRunTime::GetInstance()->GetExePath() + "File\\excel\\" + (isCN ? "ECUMenu_cn.bin" : "ECUMenu_en.bin");
CString PATH_ECUMenuHead = CRunTime::GetInstance()->GetExePath() + "File\\ECUMenuHead.bin";

CString PATH_KeyHtml = CRunTime::GetInstance()->GetExePath() + "File\\Htmls\\";
CString PATH_OperateGuide = CRunTime::GetInstance()->GetExePath() + "File\\OperateGuides\\";
CString PATH_RemoteRelearn = CRunTime::GetInstance()->GetExePath() + "File\\RemoteRelearn\\";

struct EnumIndex;
struct MenuSQL;
struct Menu;
struct ECUMenu;
struct Text;
struct KeyMenu;
struct OperateGuide;
struct RemoteRelearn;

std::vector<EnumIndex> vec_EnumIndex;
std::vector<MenuSQL> vec_MenuSQL;
std::map<CString, Menu> map_Menu;
std::map<CString, int> map_Menu_IDID_cnt;
std::vector<ECUMenu> vec_ECUMenu;
std::map<CString, CString> map_ECU_Menu;
std::map<CString, KeyMenu> map_KeyMenu;
std::vector<Text> vec_Text;
std::map<CString, CString> map_Text;
std::map<CString, CString> map_Text_cn;
std::set<Text> set_Text;
std::vector<OperateGuide> vec_OperateGuide;
std::vector<RemoteRelearn> vec_RemoteRelearn;

struct EnumIndex {
	CString IDID;
	CString Index;
	CString UpperName;
	CString MaxiSysName;
	CString EnumType;
	CString EnumName;
	CString EnumValue;
	CString MenuText;
	CString TextID;
	CString TextID_HEX;
	CString ID;
};

struct MenuSQL {
	CString IDID;
	CString xx;
	CString TextID_HEX;
	CString range;
};

struct Menu {
	CString IDID;
	CString Index;	// 序列号
	CString Area;	// 区域
	CString VehicleType;	// 车辆类型
	CString	Brand;	// 品牌
	CString	SubBrand;	// 子品牌
	CString Mode;	//车型
	CString cn_Mode;	// 车型(中文)	
	CString Year;	// 年款
	CString KeyType;	// 钥匙类型
	CString Characteristics;	// 特征
	CString ModelCode; // Model  Code
	CString ECUs;	// 防盗功能
	CString SpecialFunction;	// 特殊功能
	CString Key;
	CString RemoteRelearnType;
	CString Help;
	CString IS_SCAN_ECUS;
	CString IS_PinCode; // 是否需要密码
	CString Password_acquisition_method;	// 密码获取方法
	CString maximum_number_of_keys;	// 车辆最多支持钥匙数量
	CString Vehicle_coil_position; // 车辆线圈位置
	CString OBD_interface_location;	// OBD接口位置
	CString Key_matching_sensing_zone;	// 钥匙匹配感应区
	CString Sensing_zone_location; // 感应区位置
	CString Whether_it_is_verified_in_real_vehicles; // 是否实车验证
	CString Supported_device_types; // 支持设备类型
	CString IsRelease;
	CString Upgrade_or_test_instructions; // 升级/测试说明
	CString MODEL_PIC;
	CString KEY_PIC;
	CString cn_KeyDescription;	// 钥匙说明(CN)
	CString en_KeyDescription;	// 钥匙说明(EN)
	CString other; // 其他
	CString SupportedLanguages; // 支持语言
	CString Support_anti_theft_scanning_UI;	// 支持防盗扫描UI
	CString Topology_map_file_name;	// 拓扑图文件名
	CString Support_ECU_replacement; // 支持ECU更换
	CString DEMO_is_supported; // 支持DEMO
};

struct ECUMenu {
	CString IDID;
	CString Index;	// 序列号
	CString Ecu_Or_Function_Type;	// 所属功能，一般是控制单元
	CString cn_Ecu_Or_Function_Name; // Ecu/Function Name[CN]
	CString Manufactuer; // 就是该功能的名字。一般是防盗/智能系统、防盗系统、遥控系统
	CString Feature; //功能的名字的补充，会和上面一起连接显示
	CString Note;
	CString PartNum;
	CString ProtocolDoc;	// 这个就是ECUs
	CString TaskID; // 这个是功能的ID，一般是数字，此数字就是代表着对应的功能，可以理解我们的第一个菜单下标
	CString Protocol;	// 一般是排气、油箱、发动机类型
	CString Whether_to_support_all_drops;	// 是否支持全丢
	CString Whether_it_is_a_common_feature; // 是否为常用功能
	CString Whether_to_participate_in_ECUS_scanning; // 是否参与ECUS扫描
	CString MCUModel;	// MCU型号
	CString EEPROMModel; // EEPROM型号
	CString ECU_subfunction_ID; // ECU子功能ID
	CString Supported_device_types;	// 支持设备类型
	CString Whether_it_is_an_ECU_replacement_function; // 是否为ECU更换功能
	CString Whether_it_is_a_DEMO_function;	// 是否为DEMO功能
};

struct Text {
	CString IDID;
	CString data;
};

struct KeyMenu {
	CString IDID;
	CString index;
	CString KeyMark;	// Key 钥匙代号
	CString Whether_the_chip_is_dedicated;	// 芯片是否专用
	CString ChipNumber_CN;	// 芯片编号（CN）
	CString ChipNumber_EN;	// 芯片编号（EN）
	CString ChipModel;		// 芯片型号
	CString rate;			// 频率
	CString Key_billet_number_CN;	// 钥匙坯号(CN)
	CString Whether_the_door_lockand_ignition_are_different_CN; // 门锁与点火是否差片(CN)
	CString Whether_the_chip_is_copyable_CN;	// 芯片是否可拷贝(CN)
};

struct OperateGuide {
	CString IDID;
	CString ECUType;
	CString sub_func; // 子功能(操作说明的内容)
	CString notice;	 // 注意事项
	std::vector<CString> vec_fun;// 操作简介
};

struct RemoteRelearn {
	CString IDID;
	CString Index;
	CString RelearnType;
	CString ID;
	CString Description;	
};

CString hashString(const std::string str) {
	std::hash<std::string> hasher;
	size_t hashValue = hasher(str);

	// 将哈希值转换为字符串
	std::string uniqueStr = std::to_string(hashValue);
	return uniqueStr.c_str();
}

CString encryptString(const std::string str) {
	unsigned char digest[SHA256_DIGEST_LENGTH];
	SHA256_CTX sha256;
	SHA256_Init(&sha256);
	SHA256_Update(&sha256, str.c_str(), str.length());
	SHA256_Final(digest, &sha256);

	std::stringstream ss;
	for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
		ss << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(digest[i]);
	}

	std::string encryptedStr = ss.str();
	return encryptedStr.c_str();
}

CString AnsiToUtf8(const char* src)
{
	int nSize = MultiByteToWideChar(CP_ACP, 0, src, -1, nullptr, 0);
	wchar_t* pWideStr = new wchar_t[nSize];
	MultiByteToWideChar(CP_ACP, 0, src, -1, pWideStr, nSize);

	nSize = WideCharToMultiByte(CP_UTF8, 0, pWideStr, -1, nullptr, 0, nullptr, nullptr);
	char* pUtf8Str = new char[nSize];
	WideCharToMultiByte(CP_UTF8, 0, pWideStr, -1, pUtf8Str, nSize, nullptr, nullptr);

	CString strResult(pUtf8Str);

	delete[] pWideStr;
	delete[] pUtf8Str;

	return strResult;
}

// UTF-8编码转为GBK编码
CString utf8_to_gbk(const char* utf8_string)
{
	// 先将UTF-8编码转为宽字符（Unicode）
	int wide_length = MultiByteToWideChar(CP_UTF8, 0, utf8_string, -1, NULL, 0);
	wchar_t* wide_string = new wchar_t[wide_length];
	MultiByteToWideChar(CP_UTF8, 0, utf8_string, -1, wide_string, wide_length);

	// 再将宽字符（Unicode）转为GBK编码
	int gbk_length = WideCharToMultiByte(CP_ACP, 0, wide_string, -1, NULL, 0, NULL, NULL);
	char* gbk_string = new char[gbk_length];
	WideCharToMultiByte(CP_ACP, 0, wide_string, -1, gbk_string, gbk_length, NULL, NULL);

	// 释放内存并返回GBK编码字符串
	delete[] wide_string;
	CString result(gbk_string);
	delete[] gbk_string;
	return result;
}

CString toReplaceHtmlName(std::string str) {
	for (int i = 0; i < str.length(); i++)
	{
		if (isdigit(str[i]))
		{
			int start = i;
			while (i < str.length() && isdigit(str[i])) {
				// 加起来小于9就不会进位
				if (str[i] <= '7') {
					str[i] += 2;
				}

				i++;
			}

			int end = i - 1;
			int num = stoi(str.substr(start, end - start + 1)) + 2;		//连续的字符串加2
			std::stringstream ss;
			ss << std::hex << num;
			std::string new_num_str = ss.str();

			for (int i = 0; i < new_num_str.length(); i++) {
				new_num_str[i] = toupper(new_num_str[i]); // 将字符转为大写
			}

			str.replace(start, end - start + 1, new_num_str);
			i = start + new_num_str.length();
		}
	}

	return str.c_str();
}

int getCharCnt(CString& str, const char c = '\t') {
	int cnt = 0;

	for (int i = 0; i < str.GetLength(); i++) {
		if (str[i] == c) {
			cnt++;
		}
	}

	return cnt;
}

CString getLineCString(CMyFile& input, int TabCnt = 11) {
	CString str;

	while (true) {
		CString data;
		input.ReadString(data);

		str += data;

		if (str.IsEmpty()) {
			return "isEmpty";
		}

		if (str.Find("IDID:") != -1) {
			str.Trim();

			// 暂时不处理IDID
			/*str = str.Mid(str.Find(":") + 1, -1);
			str.Trim();*/
			break;
		}
		str += ", ";
		if (getCharCnt(str) >= TabCnt) {
			str.Trim();
			if (str.Find('\t') == -1) {
				return "";
			}
			str = str.Mid(0, str.Find('\t'));
			str.Trim();
			break;
		}
	}

	return str;
}

bool any_EnumIndex(CString filePath = PATH + "EnumIndex.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	while (true) {
		EnumIndex enumIndex;
		CString* ptr_enumIndex = (CString*)&enumIndex;
		const unsigned int n = sizeof(EnumIndex) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			ptr_enumIndex[i] = getLineCString(input, n);

			if (ptr_enumIndex[i].Find("isEmpty") != -1) {
				return true;
			}
		}

		// EnumType(数据的类型1)必须是EVehicleMake，他的(menu-SQLID)才有效。
		if (enumIndex.EnumType.Find("EVehicleMake") != -1) {
			vec_EnumIndex.push_back(enumIndex);
		}
	}

	return true;
}

bool any_MenuSQL(CString filePath = PATH + "Menu-SQL.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	while (true) {
		MenuSQL menuSQL;
		CString* ptr_menuSQL = (CString*)&menuSQL;
		const unsigned int n = sizeof(MenuSQL) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			ptr_menuSQL[i] = getLineCString(input, 11);

			if (ptr_menuSQL[i].Find("isEmpty") != -1) {
				return true;
			}
		}

		vec_MenuSQL.push_back(menuSQL);
	}

	return true;
}

bool any_Menu(CString filePath = PATH + "Menu.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	while (true) {
		Menu menu;
		CString* ptr_menu = (CString*)&menu;
		const unsigned int n = sizeof(Menu) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			ptr_menu[i] = getLineCString(input, 11);

			if (ptr_menu[i].Find("isEmpty") != -1) {
				return true;
			}

			if (getCharCnt(ptr_menu[i], ',') == 3) {
				CString str = ptr_menu[i];
				str.Replace("0x", "");
				str.Replace(",", "");
				str.Insert(0, "IDID:0xFFFD");

				if (map_Text.count(str) > 0) {
					ptr_menu[i] = map_Text[str];
					if (ptr_menu[i].IsEmpty() || ptr_menu[i].Find("ImFlag_needTranslation") != -1) {
						if (map_Text_cn.count(str) > 0) {
							ptr_menu[i] = map_Text_cn[str];
						}
					}
				}
			}
		}

		if (!menu.Help.IsEmpty()) {
			menu.Help = toReplaceHtmlName(menu.Help.GetBuffer());
			/*if (menu.Help.GetLength() > 20) {
				menu.Help = "namescnt_" + CDataConvert::IntToDecString(names_cnt);
			}*/
		}

		if (!menu.Index.IsEmpty()) {
			menu.Index = toReplaceHtmlName(menu.Index.GetBuffer());
		}

		menu.Index = hashString((menu.Index + (menu.Key.IsEmpty() ? "" : menu.Key) + (menu.Help.IsEmpty() ? "" : menu.Help)).GetBuffer());
		menu.Index = ptr_ + menu.Index;

		map_Menu[menu.IDID] = menu;
	}

	return true;
}

bool any_ECUMenu(CString filePath = PATH + "ECUMenu.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	while (true) {
		ECUMenu eCUMenu;
		CString* ptr_eCUMenu = (CString*)&eCUMenu;
		const unsigned int n = sizeof(ECUMenu) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			ptr_eCUMenu[i] = getLineCString(input, 11);

			if (ptr_eCUMenu[i].Find("isEmpty") != -1) {
				return true;
			}

			if (getCharCnt(ptr_eCUMenu[i], ',') == 3) {
				CString str = ptr_eCUMenu[i];
				str.Replace("0x", "");
				str.Replace(",", "");
				str.Insert(0, "IDID:0xFFFD");

				if (map_Text.count(str) > 0) {
					ptr_eCUMenu[i] = map_Text[str];
				}
			}
		}

		vec_ECUMenu.push_back(eCUMenu);
		map_ECU_Menu[eCUMenu.ProtocolDoc] = eCUMenu.cn_Ecu_Or_Function_Name;
	}

	return true;
}

bool any_Text(CString filePath = PATH + "cn_text.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	while (true) {
		Text text;
		CString* ptr_text = (CString*)&text;
		const unsigned int n = sizeof(Text) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			ptr_text[i] = getLineCString(input, 11);

			if (ptr_text[i].Find("isEmpty") != -1) {
				bool flag = map_Text.size() > 0;

				for (auto& e : vec_Text) {
					if (!flag) {
						map_Text[e.IDID] = e.data;
					}
					
					// 中文会冗余，英文库不足调用的
					if (filePath.Find("cn_text.tab.txt") != -1) {
						map_Text_cn[e.IDID] = e.data;
					}
				}
				vec_Text.clear();

				return true;
			}

			if (i == 0 && ptr_text[i].Find("IDID:") == -1) {
				vec_Text[vec_Text.size() - 1].data += "," + ptr_text[i];
				--i;
			}
		}

		vec_Text.push_back(text);
	}

	return true;
}

bool any_KeyMenu(CString filePath = PATH + "KeyMenu.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	while (true) {
		KeyMenu keyMenu;
		CString* ptr_keyMenu = (CString*)&keyMenu;
		const unsigned int n = sizeof(KeyMenu) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			ptr_keyMenu[i] = getLineCString(input, 11);

			if (ptr_keyMenu[i].Find("isEmpty") != -1) {
				return true;
			}

			if (getCharCnt(ptr_keyMenu[i], ',') == 3) {
				CString str = ptr_keyMenu[i];
				str.Replace("0x", "");
				str.Replace(",", "");
				str.Insert(0, "IDID:0xFFFD");

				if (map_Text.count(str) > 0) {
					ptr_keyMenu[i] = map_Text[str];

					// 门锁与点火是否差片   芯片是否可拷贝
					if (!isCN && (i == 8 || i == 9 || i == 10)) {
						if (ptr_keyMenu[i].IsEmpty() || ptr_keyMenu[i].Find("ImFlag_needTranslation") != -1) {
							if (map_Text_cn.count(str) > 0) {
								ptr_keyMenu[i] = map_Text_cn[str];
							}
						}
					}
				}
			}
		}

		map_KeyMenu[keyMenu.KeyMark] = keyMenu;
	}

	return true;
}

CString getText(CString row_data) {
	if (getCharCnt(row_data, ',') == 3) {
		CString str = row_data;
		str.Replace("0x", "");
		str.Replace(",", "");
		str.Insert(0, "IDID:0xFFFC");

		if (map_Text.count(str) > 0) {
			if (map_Text[str].IsEmpty() && map_Text_cn.count(str) > 0) {
				return map_Text_cn[str];
			}
			return map_Text[str];
		}
		else {
			return "";
		}
	}
	
	return row_data;
}

bool any_OperateGuide(CString filePath = PATH + "OperateGuide.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	CString row_data;
	OperateGuide *operateGuide = operateGuide = new OperateGuide();

	int n = 0;
	while (true) {
		input.ReadString(row_data);
		row_data.Trim();

		if (row_data.IsEmpty()) {
			if (n++) {
				vec_OperateGuide.push_back(*operateGuide);
				delete operateGuide;
			}
			break;
		}

		if (row_data.Find("IDID:") != -1) {
			if (n++) {
				vec_OperateGuide.push_back(*operateGuide);
				delete operateGuide;
				operateGuide = new OperateGuide();
			}

			operateGuide->IDID = row_data;

			CString* ptr_OperateGuide = (CString*)(operateGuide) + 1;
			for (int i = 0; i < 3; i++) {
				input.ReadString(row_data);
				row_data.Trim();
				row_data = row_data.Mid(0, row_data.Find('\t'));
				ptr_OperateGuide[i] = getText(row_data);
			}
		}
		else {
			row_data = row_data.Mid(0, row_data.Find('\t'));
			row_data = getText(row_data);

			if (!row_data.IsEmpty()) {
				operateGuide->vec_fun.push_back(row_data);
			}
		}
	}

	return true;
}

bool any_RemoteRelearn(CString filePath = PATH + "RemoteRelearn.tab.txt") {
	CMyFile input;
	if (!input.Open(filePath, CMyFile::modeRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	while (true) {
		RemoteRelearn remoteRelearn;
		CString* ptr_remoteRelearn = (CString*)&remoteRelearn;
		const unsigned int n = sizeof(RemoteRelearn) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			ptr_remoteRelearn[i] = getLineCString(input, 11);

			if (ptr_remoteRelearn[i].Find("isEmpty") != -1) {
				return true;
			}

			if (getCharCnt(ptr_remoteRelearn[i], ',') == 3) {
				CString str = ptr_remoteRelearn[i];
				str.Replace("0x", "");
				str.Replace(",", "");
				str.Insert(0, "IDID:0xFFFD");

				if (map_Text.count(str) > 0) {
					ptr_remoteRelearn[i] = map_Text[str];
					if (ptr_remoteRelearn[i].IsEmpty() && map_Text_cn.count(str) > 0) {
						ptr_remoteRelearn[i] = map_Text_cn[str];
					}
				}
			}
		}
		vec_RemoteRelearn.push_back(remoteRelearn);
	}

	return true;
}

CString to0x(CString str) {
	str.Replace("0x", "");

	for (int i = str.GetLength(); i < 8; i++) {
		str.Insert(0, "0");
	}

	CString s;
	for (int i = 0; i < str.GetLength(); i += 2) {
		s += "0x" + str.Mid(i, 2) + ",";
	}

	s.Delete(s.GetLength() - 1, 1);

	return s;
}

std::vector<MenuSQL> getMenuSQLs(CString& menu_SQLID) {
	std::vector<MenuSQL> MenuSQLs;

	for (auto& menuSQL : vec_MenuSQL) {
		if (menu_SQLID.Compare(menuSQL.TextID_HEX) == 0) {
			MenuSQLs.push_back(menuSQL);
		}
	}

	return MenuSQLs;
}

std::vector<Menu> getMenus(std::vector<MenuSQL>& MenuSQLs) {
	std::vector<Menu> Menus;

	for (auto& menuSQL : MenuSQLs) {

		for (int i = 0; i < menuSQL.range.GetLength(); ) {
			int start_index = menuSQL.range.Find("~", i);
			CString start = menuSQL.range.Mid(i, start_index - i);
			int end_index = menuSQL.range.Find(" ", start_index);
			CString end = menuSQL.range.Mid(start_index + 1, end_index - start_index);

			int s = CDataConvert::StrToInt(start);
			int e = CDataConvert::StrToInt(end);

			for (; s <= e; s++) {
				CString IDID = "IDID:0x";

				CString str = CDataConvert::UIntToString(s, 16);
				for (int j = str.GetLength(); j < 8; j++) {
					str.Insert(0, "0");
				}

				IDID += str;

				if (map_Menu.count(IDID) > 0) {
					Menus.push_back(map_Menu[IDID]);
				}
			}

			if (end_index != -1) {
				i = end_index + 1;
			}
			else {
				break;
			}
		}
	}

	return Menus;
}

D_BOOL outputKeyHtml(Menu& menu, KeyMenu& keyMenu, CString filePath = PATH_KeyHtml) {
	CMyFile output;

	if (menu.Help.IsEmpty()) {
		return true;
	}

	filePath += (isCN ? "CN_" : "EN_") + menu.Index + ".html";
	if (!output.Open(filePath, CMyFile::modeCreate)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	// 写html 头
	output.WriteString("<!DOCTYPE html>\n");
	output.WriteString("<html>\n");
	output.WriteString("<head>\n");

	CString title = "<title>";
	title += menu.Help;
	title += "</title>";
	output.WriteString(title + "\n");
	output.WriteString("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n");
	output.WriteString("<link rel=\"stylesheet\" href=\"../style.css\">\n");
	//output.WriteString("<link rel=\"stylesheet\" href=\"../style.min.css\">\n");
	output.WriteString("</head>\n");
	output.WriteString("<body>\n");
	output.WriteString("<table>\n");

	CString Key_matching_information_date[] = { menu.IS_PinCode, menu.Password_acquisition_method, menu.maximum_number_of_keys, menu.Key_matching_sensing_zone, menu.Sensing_zone_location};
	CString Key_matching_information[] = { "需要密码\\:\\ ", "密码来源\\:\\ ", "最多支持钥匙数量\\:\\ ", "钥匙感应区\\:\\ ", "感应区位置\\:\\ " };
	CString Key_matching_information_en[] = { "PinCode Required\\:\\ ", "PinCode Source\\:\\ ", "Maximum number of keys\\:\\ ", "Key sensing position\\:\\ ", "感应区位置\\:\\ " };

	if (!isCN) {
		for (int i = 0; i < sizeof(Key_matching_information) / sizeof(CString); i++) {
			Key_matching_information[i] = Key_matching_information_en[i];
		}
	}

	//if (!menu.IS_PinCode.IsEmpty() || !menu.Password_acquisition_method.IsEmpty() || !menu.maximum_number_of_keys.IsEmpty() || !menu.Key_matching_sensing_zone.IsEmpty() || !menu.Sensing_zone_location.IsEmpty()) {
	{
		//写钥匙匹配信息
		if (!menu.IS_PinCode.IsEmpty()) {
			CString utf_IS_PinCode = AnsiToUtf8(menu.IS_PinCode.GetBuffer());

			if (isCN) {
				if (utf_IS_PinCode.Compare("N") == 0) {
					char no_ansi[3] = { 0xB7, 0xF1, 0x00 };
					Key_matching_information_date[0] = CString(no_ansi);
					Key_matching_information_date[1].Empty();
				}
				else if (utf_IS_PinCode.Compare("Y") == 0) {
					char yes_ansi[3] = { 0xCA, 0xC7, 0x00 };
					Key_matching_information_date[0] = CString(yes_ansi);
				}
			}
			else {
				if (utf_IS_PinCode.Compare("N") == 0) {
					Key_matching_information_date[0] = "No";
					Key_matching_information_date[1].Empty();
				}
				else if (utf_IS_PinCode.Compare("Y") == 0) {
					Key_matching_information_date[0] = "Yes";
				}
			}
		}

		for (int i = 0; i < sizeof(Key_matching_information) / sizeof(CString); i++) {
			// 感应区位置不用，这里位置对应着图片的位置
			if (i == sizeof(Key_matching_information) / sizeof(CString) -1) {
				continue;
			}

			CString tr = "<tr>\n<td>" + Key_matching_information[i] + "</td>\n<td>";
			if (!Key_matching_information_date[i].IsEmpty() && Key_matching_information_date[i].Find("ImFlag_needTranslation") == -1) {
				tr += AnsiToUtf8(Key_matching_information_date[i].GetBuffer());
			}

			tr += "</td>\n</tr>";
			tr.Replace("\\:\\ ", "");

			output.WriteString(tr + "\n");
		}
	}

	CString Key_information_data[] = { isCN ? menu.cn_KeyDescription : menu.en_KeyDescription, keyMenu.Whether_the_chip_is_dedicated,
					isCN ? keyMenu.ChipNumber_CN : keyMenu.ChipNumber_EN, keyMenu.ChipModel, keyMenu.rate, keyMenu.Key_billet_number_CN, keyMenu.Whether_the_door_lockand_ignition_are_different_CN, keyMenu.Whether_the_chip_is_copyable_CN, "", ""};
	CString Key_information[] = { "钥匙类型\\:\\ ", "经销商钥匙\\:\\ ", "芯片型号\\:\\ ", "芯片型号\\:\\ ", "遥控频率\\:\\ ", "钥匙坯号\\:\\ ", "门锁与点火是否差片\\:\\ ", "芯片可拷贝\\:\\ ", "遥控匹配\\:\\ ", "需要工作钥匙\\:\\ "};
	CString Key_information_en[] = { "Key Type\\:\\ ", "Pre-code Key\\:\\ ", "Transponder Type\\:\\ ", "芯片型号\\:\\ ", "Remote Frequency\\:\\ ", "Number of key blank\\:\\ ", "Are the door lock and ignition faulty\\:\\ ", "Is the transponder copyable\\:\\ ", "Program Remotes\\:\\ ", "Working key Required\\:\\ "};

	if (!isCN) {
		for (int i = 0; i < sizeof(Key_information) / sizeof(CString); i++) {
			Key_information[i] = Key_information_en[i];
		}
	}

	/*if (!Key_information_data[0].IsEmpty() || !Key_information_data[1].IsEmpty() || !Key_information_data[2].IsEmpty()
		|| !Key_information_data[3].IsEmpty() || !Key_information_data[4].IsEmpty() || !Key_information_data[5].IsEmpty() || !Key_information_data[6].IsEmpty() || !Key_information_data[7].IsEmpty()) {*/
	{
		// 钥匙信息
		for (int i = 0; i < sizeof(Key_information) / sizeof(CString); i++) {
			// 芯片型号 一直都是空的，暂时不要
			if (i == 3) {
				continue;
			}

			CString tr = "<tr>\n<td>" + Key_information[i] + "</td>\n<td>";
			if (!Key_information_data[i].IsEmpty() && Key_information_data[i].Find("ImFlag_needTranslation") == -1) {
				
				CString data_= AnsiToUtf8(Key_information_data[i].GetBuffer());

				// 可删除
				if (!isCN && i == 5) {
					char number_[] = { 0xBA, 0xC5, 0 };
					Key_information_data[i].Replace(number_, " Number");
					data_ = AnsiToUtf8(Key_information_data[i].GetBuffer());
				}

				if (!isCN && (i == 6 || i == 7)) {
					char yes_[] = { 0xCA, 0xC7, 0 };
					char no_[] = {0xB7, 0xF1, 0};

					if (Key_information_data[i].CompareNoCase(yes_) == 0) {
						data_ = "Yes";
					}
					else if (Key_information_data[i].CompareNoCase(no_) == 0) {
						data_ = "No";
					}
				}

				tr += data_;
			}

			tr += "</td>\n</tr>";
			tr.Replace("\\:\\ ", "");

			output.WriteString(tr + "\n");
		}
	}

	output.WriteString("</table>\n");
	output.WriteString("</body>\n");
	output.WriteString("</html>\n");
	output.Close();
}

void splitStr(CString& data, CString c, std::vector<CString>& vec) {
	int c_len = c.GetLength();
	D_I32 start = 0;
	D_I32 end = 0;
	//adsMessageBox(STD_TEXT_INFORMATION, data, DF_MB_OK);
	while (end < data.GetLength()) {
		end = data.Find(c, start);

		CString str = data.Mid(start, end - start);

		vec.push_back(str);
		start = end + c_len;
		if (end == -1) {
			break;
		}
	}
}

CString getECUmenuFunctionName(CString &ECUs) {
	std::vector<CString> protocolDocs;
	CString functionNames;

	splitStr(ECUs, ", ", protocolDocs);

	for (auto& protocolDoc : protocolDocs) {
		if (map_ECU_Menu.count(protocolDoc) > 0) {
			functionNames += map_ECU_Menu[protocolDoc] + ", ";
		}
	}

	if (!functionNames.IsEmpty()) {
		functionNames.Delete(functionNames.GetLength() - 2, 2);
	}

	return functionNames;
}

D_BOOL outputMenus(std::vector<Menu>& menus, CString filePath = PATH_Menu) {
	CMyFile output;
	static bool MenuHead = false;

	if (!output.Open(filePath, CMyFile::AddTxtReadWrite)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	if (!MenuHead) {
		CMyFile inputMenuHead;
		if (!inputMenuHead.Open(PATH_MenuHead, CMyFile::TxtRead)) {
			adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
			return false;
		}
		CString data;
		inputMenuHead.ReadString(data);
		output.WriteString(data + "\n");
		MenuHead = true;
		inputMenuHead.Close();
	}

	for (auto& menu : menus) {
		if (map_Menu_IDID_cnt.count(menu.IDID) > 0) {
			continue;
		}

		CString* ptr_menu = (CString*)&menu;
		const unsigned int n = sizeof(Menu) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			if (!ptr_menu[i].IsEmpty()) {
				output.Write(ptr_menu[i].GetBuffer(0), ptr_menu[i].GetLength());

				//防盗功能多加一列
				if (i == 12) {
					char tab = '\t';
					output.Write(&tab, 1);
					CString functionNames = getECUmenuFunctionName(ptr_menu[i]);

					if (!functionNames.IsEmpty()) {
						output.Write(functionNames.GetBuffer(), functionNames.GetLength());
					}
				}
			}
			char tab = '\t';
			output.Write(&tab, 1);
		}

		// 写KeyMenu
		if (map_KeyMenu.count(menu.Key) > 0) {
			KeyMenu keyMenu = map_KeyMenu[menu.Key];

			// 无需展示
			/*CString* ptr_keyMenu = (CString*)&keyMenu;
			const unsigned int n = sizeof(KeyMenu) / sizeof(CString);
			for (int i = 0; i < n; i++) {
				if (!ptr_keyMenu[i].IsEmpty()) {
					output.Write(ptr_keyMenu[i].GetBuffer(0), ptr_keyMenu[i].GetLength());
				}
				char tab = '\t';
				output.Write(&tab, 1);
			}*/

			outputKeyHtml(menu, keyMenu);
		}

		char line[] = { '\n' };
		output.Write(line, sizeof(line));

		map_Menu_IDID_cnt[menu.IDID]++;
	}

	output.Close();

	return true;
}

D_BOOL outputECUMenu(CString filePath = PATH_ECUMenu) {
	CMyFile output;
	CMyFile inputMenuHead;

	if (!output.Open(filePath, CMyFile::TxtCreate)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	if (!inputMenuHead.Open(PATH_ECUMenuHead, CMyFile::TxtRead)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}
	CString data;
	inputMenuHead.ReadString(data);
	output.WriteString(data + "\n");
	inputMenuHead.Close();

	for (auto& eCUMenu : vec_ECUMenu) {
		CString* ptr_eCUMenu = (CString*)&eCUMenu;
		const unsigned int n = sizeof(ECUMenu) / sizeof(CString);

		for (int i = 0; i < n; i++) {
			if (!ptr_eCUMenu[i].IsEmpty()) {
				output.Write(ptr_eCUMenu[i].GetBuffer(0), ptr_eCUMenu[i].GetLength());
			}
			char tab = '\t';
			output.Write(&tab, 1);
		}
		char line[] = { '\n' };
		output.Write(line, sizeof(line));;
	}

	output.Close();

	return true;
}

D_BOOL outOperateGuides(CString filePath = PATH_OperateGuide) {
	for (int i = 0; i < vec_OperateGuide.size(); i++) {
		if (vec_OperateGuide[i].notice.IsEmpty() && vec_OperateGuide[i].sub_func.IsEmpty() && (vec_OperateGuide[i].vec_fun.size() == 0)) {
			continue;
		}

		CMyFile output;
		output.Open(PATH_OperateGuide + vec_OperateGuide[i].ECUType + ".html", CMyFile::modeCreate);

		//output.WriteString(vec_OperateGuide[i].IDID);
		//output.WriteString(vec_OperateGuide[i].ECUType);

		// 写html 头
		output.WriteString("<!DOCTYPE html>\n");
		output.WriteString("<html>\n");
		output.WriteString("<head>\n");

		CString title = "<title>";
		title += vec_OperateGuide[i].ECUType;
		title += "</title>";
		output.WriteString(title + "\n");
		output.WriteString("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n");
		output.WriteString("<link rel=\"stylesheet\" href=\"../style.css\">\n");
		output.WriteString("</head>\n");
		output.WriteString("<body>\n");

		if (!vec_OperateGuide[i].sub_func.IsEmpty()) {
			//vec_OperateGuide[i].sub_func.Replace(" ", "\n\t");
			//output.WriteString(utf8_to_gbk("<h2>操作说明</h2>\n<hr />\n\t") + vec_OperateGuide[i].sub_func + "\n");
			output.WriteString(utf8_to_gbk("<h2>操作说明</h2>\n<hr />\n"));

			std::vector<CString> li_s;
			splitStr(vec_OperateGuide[i].sub_func, ", ", li_s);
			output.WriteString("<ul>\n");
			for (auto li_ : li_s) {
				if (li_.IsEmpty()) {
					continue;
				}

				output.WriteString("<li>" + li_ + "</li>\n");
			}
			output.WriteString("</ul>\n");
		}

		std::vector<CString> fc_vec;
		CString str_fc = vec_OperateGuide[i].sub_func;
		const char left_char[] = { 0xA1, 0xBE, 0x00};
		const char right_char[] = { 0xA1, 0xBF, 0x00 };
		CString left_str(left_char);
		CString right_str(right_char);

		int start_ = 0;
		int end_ = 0;

		while (true) {
			start_ = str_fc.Find(left_str, start_);
			end_ = str_fc.Find(right_str, start_);

			if (start_ == -1) {
				break;
			}

			fc_vec.push_back(str_fc.Mid(start_ + 2, end_ - start_ - 2));
			start_ = end_;
		}

		if (vec_OperateGuide[i].vec_fun.size() != 0 && fc_vec.size() != 0) {
			CString operation_info("<h2>操作简介\\</h2>\n<hr />\n");
			operation_info.Replace("\\", "");
			output.WriteString(utf8_to_gbk(operation_info.GetBuffer()));
			for (int j = 0; j < vec_OperateGuide[i].vec_fun.size(); j++) {
				if (!vec_OperateGuide[i].vec_fun[j].IsEmpty()) {
					//vec_OperateGuide[i].vec_fun[j].Replace(" ", "\n\t\t");
					//output.WriteString(utf8_to_gbk("\t功能 ") + CDataConvert::IntToDecString(j + 1) + ":\n\t\t" + vec_OperateGuide[i].vec_fun[j] + "\n");
					if (fc_vec.size() != 0) {
						//output.WriteString("\t<h3>" + fc_vec[j] + "</h3>\n\t\t" + vec_OperateGuide[i].vec_fun[j] + "\n");
						output.WriteString("<h3>" + fc_vec[j] + "</h3>\n");
						
						std::vector<CString> li_s;
						splitStr(vec_OperateGuide[i].vec_fun[j], ", ", li_s);
						output.WriteString("<ul>\n");
						for (auto li_ : li_s) {
							if (li_.IsEmpty()) {
								continue;
							}

							if (li_.Find(".jpg") != -1 || li_.Find(".png") != -1) {
								output.WriteString("<img src=\"../imgs/" + li_ + "\" /><br />\n");
							}
							else {
								output.WriteString("<li>" + li_ + "</li>\n");
							}
						}
						output.WriteString("</ul>\n");
					}
				}
			}
		}

		if (!vec_OperateGuide[i].notice.IsEmpty()) {
			//vec_OperateGuide[i].notice.Replace(" ", "\n\t");
			//output.WriteString(utf8_to_gbk("<h2>注意事项</h2>\n<hr />\n\t") + vec_OperateGuide[i].notice + "\n\n");
			output.WriteString(utf8_to_gbk("<h2>注意事项</h2>\n<hr />\n"));

			std::vector<CString> li_s;
			splitStr(vec_OperateGuide[i].notice, ", ", li_s);
			output.WriteString("<ul>\n");
			for (auto li_ : li_s) {
				if (li_.IsEmpty()) {
					continue;
				}

				output.WriteString("<li>" + li_ + "</li>\n");
			}
			output.WriteString("</ul>\n");
		}

		output.WriteString("</body>\n");
		output.WriteString("</html>\n");

		output.Close();
	}

	return TRUE;
}

D_BOOL outputRemoteRelearn(CString filePath = PATH_RemoteRelearn) {
	for (auto& remoteRelearn : vec_RemoteRelearn) {
		//如果id为空可以认为无效类型
		if (remoteRelearn.RelearnType.IsEmpty() || remoteRelearn.ID.IsEmpty() || remoteRelearn.Description.IsEmpty()) {
			continue;;
		}

		CMyFile output;
		output.Open(PATH_RemoteRelearn + remoteRelearn.RelearnType + ".html", CMyFile::modeCreate);

		// 写html 头
		output.WriteString("<!DOCTYPE html>\n");
		output.WriteString("<html>\n");
		output.WriteString("<head>\n");

		CString title = "<title>";
		title += remoteRelearn.RelearnType;
		title += "</title>";
		output.WriteString(title + "\n");
		output.WriteString("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n");
		output.WriteString("<link rel=\"stylesheet\" href=\"../style.css\">\n");
		output.WriteString("</head>\n");
		output.WriteString("<body>\n");

		std::vector<CString> li_s;
		splitStr(remoteRelearn.Description, ", ", li_s);
		output.WriteString("<ul>\n");
		for (auto li_ : li_s) {
			if (li_.IsEmpty()) {
				continue;
			}

			if (li_.Find(".jpg") != -1 || li_.Find(".png") != -1) {
				output.WriteString("<img src=\"../imgs/" + li_ + "\" /><br />\n");
			}
			else {
				output.WriteString("<li>" + li_ + "</li>\n");
			}
		}
		output.WriteString("</ul>\n");

		output.WriteString("</body>\n");
		output.WriteString("</html>\n");

		output.Close();
	}

	return true;
}

D_BOOL outputText(CString filePath = "CN_TEXT.bin") {
	CMyFile output;
	filePath.Insert(0, CRunTime::GetInstance()->GetExePath());

	if (!output.Open(filePath, CMyFile::modeCreate)) {
		adsMessageBox(STD_TEXT_INFORMATION, filePath + " open failed", DF_MB_OK);
		return false;
	}

	for (auto& e : set_Text) {
		CString id_ = e.IDID;
		id_.Replace("IDID:0x", "");

		CString id;

		for (int i = 0; i < id_.GetLength(); i += 2) {
			id += "0x" + id_.Mid(i, 2) + ",";
		}

		id.Delete(id.GetLength() - 1);


		CString data = e.data;
		data.Replace("\"", "'");
		data.Replace("\\", " ");

		output.WriteString(id + "\t\t\"" + data + "\"\n");
	}

	output.Close();

	return true;
}

void test() {
	/*if (any_Text()) {
		if (any_OperateGuide()) {
			outOperateGuides();
		}
	}*/

	if (any_Text()) {
		if (any_RemoteRelearn()) {
			outputRemoteRelearn();
		}
	}
}

D_ErrorCode CHARLEY::MainEntrance(CString strTitle)
{
	//test();

	/*删除目录下所有文件及目录本身*/
	CRWFile::DelDir(CRunTime::GetInstance()->GetExePath() + "File\\Htmls", true);
	CRWFile::DelDir(CRunTime::GetInstance()->GetExePath() + "File\\OperateGuides", true);
	CRWFile::DelDir(CRunTime::GetInstance()->GetExePath() + "File\\RemoteRelearn", true);

	//用来创建PATH_Menu文件
	CMyFile PATH_Menu_output;
	PATH_Menu_output.Open(PATH_Menu, CMyFile::TxtCreate);
	PATH_Menu_output.Close();

	if ((isCN ? true : any_Text(PATH + "en_text.tab.txt") ) && any_Text() && any_EnumIndex() && any_MenuSQL() && any_Menu() && any_ECUMenu() && any_KeyMenu()) {
		for (auto& enumIndex : vec_EnumIndex) {
			CString menu_SQLID = to0x(enumIndex.TextID_HEX);

			/*if (menu_SQLID.Compare("0x00,0x80,0x00,0xEA") == 0) {
				int a = 2;*/

			std::vector<MenuSQL> MenuSQLs = getMenuSQLs(menu_SQLID);
			if (MenuSQLs.size() <= 0) {
				continue;
			}
			std::vector<Menu> menus = getMenus(MenuSQLs);
			outputMenus(menus);
		}
	}

	outputECUMenu();
	
	if (any_OperateGuide()) {
		outOperateGuides();
	}

	if (any_RemoteRelearn()) {
		outputRemoteRelearn();
	}

	return CErrorCode::EC_SUCCESS;
}

D_ErrorCode CHARLEY::MainProcess(D_U32 uTaskID, CString strTitle)
{

	return CErrorCode::EC_SUCCESS;
}

D_ErrorCode CHARLEY::MainEntrance(CString uTaskID, CString strTitle)
{
	return D_ErrorCode();
}