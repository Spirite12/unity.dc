using UnityEngine;
using System.Collections;

namespace CS.AudioToolkit
{
    public class PlayMusicPlaylist : AudioTriggerBase
    {
        public string playListName = "Default";
        public AudioChannelType channel = AudioChannelType.Music;

        protected override void _OnEventTriggered()
        {
            AudioController.PlayPlaylist( playListName, channel );
        }
    }
}