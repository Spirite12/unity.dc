using DCFrame;

public class CacheInit {

    public static void Init() {
        CacheMgr.GameInit(GetPlayerId, GetServerId, GetAccountId);
    }
    
    public static string GetPlayerId() {
        return "";
    }
        
    public static string GetAccountId() {
        return "";
    }
        
    public static string GetServerId() {
        return "";
    }
}
