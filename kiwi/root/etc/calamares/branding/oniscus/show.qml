/* Oniscus installer slideshow: one dark slide with the mascot. */
import QtQuick 2.15
import calamares.slideshow 1.0

Presentation {
    id: presentation

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#121519"
        }
        Image {
            id: mascot
            source: "logo.svg"
            width: 160; height: 160
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -40
        }
        Text {
            anchors.top: mascot.bottom
            anchors.topMargin: 24
            anchors.horizontalCenter: parent.horizontalCenter
            color: "#E6E9EC"
            font.pixelSize: 18
            text: qsTr("Installing Oniscus. This can take a few minutes.")
        }
    }

    function onActivate() { }
    function onLeave() { }
}
