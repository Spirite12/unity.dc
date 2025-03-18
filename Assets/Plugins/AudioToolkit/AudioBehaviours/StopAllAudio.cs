using UnityEngine;
using System.Collections;

namespace CS.AudioToolkit
{
    public class StopAllAudio : AudioTriggerBase
    {
        public float fadeOut = 0;

        protected override void _OnEventTriggered()
        {
            AudioController.StopAll( fadeOut );
        }
    }
}