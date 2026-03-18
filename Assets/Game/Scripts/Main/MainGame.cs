using Cysharp.Threading.Tasks;
using DCFrame;
using UnityEngine;

namespace Game {
    public class MainGame : MonoSingleton<MainGame> {
        private void Awake() {
            RedTipConst.Init();
            CacheInit.Init();
        }

        private async UniTask Start() {
            // 红点
            RedTipMain redTip = new RedTipMain(RedTipConst.RedTipMain, null);
            RedTipMgr.Init(redTip);
            // 音乐
            string path = Asset.GetPrefabPath("AudioToolkit/AudioControllerMain", Asset.PrefixPath.Settings);
            GameObject prefab = await Asset.LoadAsset<GameObject>(path);
            Instantiate(prefab);
        }

        protected override void OnDestroy() {
            RedTipMgr.Destroy();
        }
    }
}
