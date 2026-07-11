using Cysharp.Threading.Tasks;
using DCFrame;
using UnityEngine;

namespace Game {
    public class MainGame : MonoSingleton<MainGame> {
        private void Awake() {
            RedTipConst.Init();
            CacheInit.Init();
        }

        private void Start() {
            InitializeAsync().Forget();
        }

        /// <summary>
        /// 初始化游戏数据
        /// </summary>
        private async UniTask InitializeAsync() {
            // 红点
            RedTipMain redTip = new RedTipMain(RedTipConst.RedTipMain, null);
            RedTipMgr.Init(redTip);
            // 音乐
            string path = Asset.GetPrefabPath("AudioToolkit/AudioControllerMain", Asset.PrefixPath.Settings);
            GameObject prefab = await LoadAsset<GameObject>(path);
            if (prefab != null) {
                Instantiate(prefab);
            }
        }

        protected override void OnDestroy() {
            RedTipMgr.Destroy();
            base.OnDestroy();
        }
    }
}
