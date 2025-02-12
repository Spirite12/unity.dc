using DCFrame;

namespace Game {
    public class MainGame : MonoSingleton<MainGame> {
        private void Awake() {
            RedTipConst.Initialization();
            TextFilter.InitFilterFile();
        }

        private void Start() {
            RedTipMain redTip = new RedTipMain(RedTipConst.RedTipMain, null);
            RedTipMgr.Init(redTip);
        }

        protected override void OnDestroy() {
            RedTipMgr.Destroy();
        }
    }
}
