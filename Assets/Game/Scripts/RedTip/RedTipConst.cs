using System;
using DCFrame;
using System.Collections.Generic;

namespace Game {
    public class RedTipConst {
        /// <summary>
        /// 游戏红点常量初始化调用
        /// </summary>
        public static void Init() {
            foreach (var keyValue in redTipTreeDic) {
                RedTipTree.redTipTreeDic.Add(keyValue.Key, keyValue.Value);
            }
            foreach (var keyValue in redTipBaseDic) {
                RedTipTree.redTipBaseDic.Add(keyValue.Key, keyValue.Value);
            }
        }

        #region 红点常量

        public const string RedTipMain = nameof(RedTipMain);

        #endregion

        #region 红点树字典

        private static readonly Dictionary<string, List<string>> redTipTreeDic = new Dictionary<string, List<string>>() { };

        #endregion

        #region 红点实例化获取
        private static readonly Dictionary<string, Func<RedTipBase>> redTipBaseDic = new Dictionary<string, Func<RedTipBase>>() { };

        #endregion
    }
}

