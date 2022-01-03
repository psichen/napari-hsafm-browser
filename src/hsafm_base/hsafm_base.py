import numpy as np
from vispy.color import Colormap


class HSAFM:
    """read asd file into np.array"""

    def __init__(self, fname):

        self.fullName = fname  # full name
        with open(self.fullName) as f:
            self.fileVersion = np.fromfile(f, "i", 1)[0]
            self.fileHeaderSize = np.fromfile(f, "i", 1)[0]
            self.frameHeaderSize = np.fromfile(f, "i", 1)[0]
            self.encNumber = np.fromfile(f, "i", 1)[0]
            self.operationNameSize = np.fromfile(f, "i", 1)[0]
            self.commentSize = np.fromfile(f, "i", 1)[0]
            self.dataTypeCh1 = np.fromfile(f, "i", 1)[0]
            self.dataTypeCh2 = np.fromfile(f, "i", 1)[0]
            self.numberFramesRecorded = np.fromfile(f, "i", 1)[0]
            self.numberFramesCurrent = np.fromfile(f, "i", 1)[0]
            self.scanDirection = np.fromfile(f, "i", 1)[0]
            self.fileName = np.fromfile(f, "i", 1)[0]
            self.xPixel = np.fromfile(f, "i", 1)[0]
            self.yPixel = np.fromfile(f, "i", 1)[0]
            self.xScanRange = np.fromfile(f, "i", 1)[0]
            self.yScanRange = np.fromfile(f, "i", 1)[0]
            self.avgFlag = np.fromfile(f, "?", 1)[0]
            self.avgNumber = np.fromfile(f, "i", 1)[0]
            self.yearRec = np.fromfile(f, "i", 1)[0]
            self.monthRec = np.fromfile(f, "i", 1)[0]
            self.dayRec = np.fromfile(f, "i", 1)[0]
            self.hourRec = np.fromfile(f, "i", 1)[0]
            self.minuteRec = np.fromfile(f, "i", 1)[0]
            self.secondRec = np.fromfile(f, "i", 1)[0]
            self.xRoundDeg = np.fromfile(f, "i", 1)[0]
            self.yRoundDeg = np.fromfile(f, "i", 1)[0]
            self.frameAcqTime = np.fromfile(f, "f", 1)[0]
            self.sensorSens = np.fromfile(f, "f", 1)[0]
            self.phaseSens = np.fromfile(f, "f", 1)[0]
            self.offset = np.fromfile(f, "i", 4)  # booked region of 12 bytes
            self.machineNum = np.fromfile(f, "i", 1)[0]

            # ADRange
            self.ADRange = np.fromfile(f, "i", 1)[0]
            if self.ADRange == 2 ** 18:
                self.ADRange = 10
            elif self.ADRange == 2 ** 17:
                self.ADRange = 5
            elif self.ADRange == 2 * 16:
                self.ADRange = 2
            else:
                print("ADRange error")
            self.ADResolution = np.fromfile(f, "i", 1)[0]

            self.xMaxScanRange = np.fromfile(f, "f", 1)[0]  # nm
            self.yMaxScanRange = np.fromfile(f, "f", 1)[0]  # nm
            self.xPizeoConstant = np.fromfile(f, "f", 1)[0]  # nm/V
            self.yPizeoConstant = np.fromfile(f, "f", 1)[0]  # nm/V
            self.zPizeoConstant = np.fromfile(f, "f", 1)[0]  # nm/V
            self.zDriveGain = np.fromfile(f, "f", 1)[0]
            self.operatorName = np.fromfile(f, "c", self.operationNameSize)
            self.comment = np.fromfile(f, "c", self.commentSize)

            # decode binary string
            self.operatorName = "".join(
                letter.decode("UTF-8") for letter in self.operatorName
            )
            self.comment = "".join(letter.decode("UTF-8") for letter in self.comment)

            # AFM data per frame
            self.voltage = []
            self.frameNumber = []
            self.frameMaxData = []
            self.frameMinData = []
            self.xOffset = []
            self.dataType = []
            self.xTilt = []
            self.yTilt = []
            self.laserFlag = []

            for _ in np.arange(self.numberFramesCurrent):
                self.frameNumber.extend(np.fromfile(f, "i", 1))
                self.frameMaxData.extend(np.fromfile(f, "u2", 1))
                self.frameMinData.extend(np.fromfile(f, "u2", 1))
                self.xOffset.extend(np.fromfile(f, "u2", 1))
                self.dataType.extend(np.fromfile(f, "u2", 1))
                self.xTilt.extend(np.fromfile(f, "f", 1))
                self.yTilt.extend(np.fromfile(f, "f", 1))
                self.laserFlag.extend(np.fromfile(f, "?", 12))

                voltage_temp = np.fromfile(f, "u2", self.xPixel * self.yPixel)
                voltage_temp = np.reshape(voltage_temp, (self.yPixel, self.xPixel))
                voltage_temp = voltage_temp[::-1][:]  # flip image upside-down
                self.voltage.append(voltage_temp)
            del voltage_temp

            self.voltage = np.array(self.voltage, dtype="float32")
            self.height = (
                -1
                * self.voltage
                * self.zPizeoConstant
                * self.zDriveGain
                * self.ADRange
                / 4096
            )
            self.height -= np.repeat(
                np.min(self.height, (1, 2)), self.yPixel * self.xPixel
            ).reshape((self.numberFramesCurrent, self.yPixel, self.xPixel))

        self.afm_lut = Colormap(
            # RGB
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0.00392156862745098, 0, 0],
                [0.00784313725490196, 0, 0],
                [0.0156862745098039, 0, 0],
                [0.0156862745098039, 0, 0],
                [0.0196078431372549, 0, 0],
                [0.0235294117647059, 0, 0],
                [0.0274509803921569, 0, 0],
                [0.0313725490196078, 0, 0],
                [0.0352941176470588, 0, 0],
                [0.0392156862745098, 0, 0],
                [0.0470588235294118, 0, 0],
                [0.0509803921568627, 0, 0],
                [0.0549019607843137, 0, 0],
                [0.0588235294117647, 0, 0],
                [0.0627450980392157, 0, 0],
                [0.0666666666666667, 0, 0],
                [0.0705882352941177, 0, 0],
                [0.0745098039215686, 0, 0],
                [0.0823529411764706, 0, 0],
                [0.0862745098039216, 0, 0],
                [0.0901960784313726, 0, 0],
                [0.0901960784313726, 0, 0],
                [0.0941176470588235, 0, 0],
                [0.0980392156862745, 0, 0],
                [0.101960784313725, 0, 0],
                [0.105882352941176, 0, 0],
                [0.113725490196078, 0, 0],
                [0.117647058823529, 0, 0],
                [0.121568627450980, 0, 0],
                [0.125490196078431, 0, 0],
                [0.129411764705882, 0, 0],
                [0.133333333333333, 0, 0],
                [0.137254901960784, 0, 0],
                [0.141176470588235, 0, 0],
                [0.149019607843137, 0, 0],
                [0.152941176470588, 0, 0],
                [0.156862745098039, 0, 0],
                [0.160784313725490, 0, 0],
                [0.164705882352941, 0, 0],
                [0.164705882352941, 0, 0],
                [0.168627450980392, 0, 0],
                [0.172549019607843, 0, 0],
                [0.180392156862745, 0, 0],
                [0.184313725490196, 0, 0],
                [0.188235294117647, 0, 0],
                [0.192156862745098, 0, 0],
                [0.196078431372549, 0, 0],
                [0.200000000000000, 0, 0],
                [0.203921568627451, 0, 0],
                [0.207843137254902, 0, 0],
                [0.215686274509804, 0, 0],
                [0.219607843137255, 0, 0],
                [0.223529411764706, 0, 0],
                [0.227450980392157, 0, 0],
                [0.231372549019608, 0, 0],
                [0.235294117647059, 0, 0],
                [0.239215686274510, 0, 0],
                [0.239215686274510, 0, 0],
                [0.247058823529412, 0, 0],
                [0.250980392156863, 0, 0],
                [0.254901960784314, 0, 0],
                [0.258823529411765, 0, 0],
                [0.262745098039216, 0, 0],
                [0.266666666666667, 0, 0],
                [0.270588235294118, 0, 0],
                [0.274509803921569, 0, 0],
                [0.282352941176471, 0, 0],
                [0.286274509803922, 0, 0],
                [0.290196078431373, 0, 0],
                [0.294117647058824, 0, 0],
                [0.298039215686275, 0, 0],
                [0.301960784313725, 0, 0],
                [0.305882352941177, 0, 0],
                [0.313725490196078, 0, 0],
                [0.317647058823529, 0, 0],
                [0.317647058823529, 0, 0],
                [0.321568627450980, 0, 0],
                [0.325490196078431, 0, 0],
                [0.329411764705882, 0, 0],
                [0.333333333333333, 0, 0],
                [0.337254901960784, 0, 0],
                [0.341176470588235, 0.00392156862745098, 0],
                [0.349019607843137, 0.0117647058823529, 0],
                [0.352941176470588, 0.0196078431372549, 0],
                [0.356862745098039, 0.0274509803921569, 0],
                [0.360784313725490, 0.0313725490196078, 0],
                [0.364705882352941, 0.0392156862745098, 0],
                [0.368627450980392, 0.0470588235294118, 0],
                [0.372549019607843, 0.0549019607843137, 0],
                [0.376470588235294, 0.0588235294117647, 0],
                [0.384313725490196, 0.0666666666666667, 0],
                [0.388235294117647, 0.0745098039215686, 0],
                [0.392156862745098, 0.0823529411764706, 0],
                [0.392156862745098, 0.0823529411764706, 0],
                [0.396078431372549, 0.0862745098039216, 0],
                [0.400000000000000, 0.0941176470588235, 0],
                [0.403921568627451, 0.101960784313725, 0],
                [0.407843137254902, 0.109803921568627, 0],
                [0.415686274509804, 0.113725490196078, 0],
                [0.419607843137255, 0.121568627450980, 0],
                [0.423529411764706, 0.129411764705882, 0],
                [0.427450980392157, 0.133333333333333, 0],
                [0.431372549019608, 0.141176470588235, 0],
                [0.435294117647059, 0.149019607843137, 0],
                [0.439215686274510, 0.156862745098039, 0],
                [0.443137254901961, 0.160784313725490, 0],
                [0.450980392156863, 0.168627450980392, 0],
                [0.454901960784314, 0.176470588235294, 0],
                [0.458823529411765, 0.184313725490196, 0],
                [0.462745098039216, 0.188235294117647, 0],
                [0.466666666666667, 0.196078431372549, 0],
                [0.466666666666667, 0.196078431372549, 0],
                [0.470588235294118, 0.203921568627451, 0],
                [0.474509803921569, 0.211764705882353, 0],
                [0.482352941176471, 0.215686274509804, 0],
                [0.486274509803922, 0.223529411764706, 0],
                [0.490196078431373, 0.231372549019608, 0],
                [0.494117647058824, 0.235294117647059, 0],
                [0.498039215686275, 0.243137254901961, 0],
                [0.501960784313726, 0.250980392156863, 0],
                [0.505882352941176, 0.258823529411765, 0],
                [0.509803921568627, 0.262745098039216, 0],
                [0.517647058823530, 0.270588235294118, 0],
                [0.521568627450980, 0.278431372549020, 0],
                [0.525490196078431, 0.286274509803922, 0],
                [0.529411764705882, 0.290196078431373, 0],
                [0.533333333333333, 0.298039215686275, 0],
                [0.537254901960784, 0.305882352941177, 0],
                [0.541176470588235, 0.313725490196078, 0],
                [0.541176470588235, 0.313725490196078, 0],
                [0.549019607843137, 0.317647058823529, 0],
                [0.552941176470588, 0.325490196078431, 0],
                [0.556862745098039, 0.333333333333333, 0],
                [0.560784313725490, 0.337254901960784, 0],
                [0.564705882352941, 0.345098039215686, 0],
                [0.568627450980392, 0.352941176470588, 0],
                [0.572549019607843, 0.360784313725490, 0],
                [0.576470588235294, 0.364705882352941, 0],
                [0.584313725490196, 0.372549019607843, 0],
                [0.588235294117647, 0.380392156862745, 0],
                [0.592156862745098, 0.388235294117647, 0],
                [0.596078431372549, 0.392156862745098, 0],
                [0.600000000000000, 0.400000000000000, 0],
                [0.603921568627451, 0.407843137254902, 0],
                [0.607843137254902, 0.415686274509804, 0],
                [0.615686274509804, 0.419607843137255, 0],
                [0.619607843137255, 0.427450980392157, 0],
                [0.619607843137255, 0.427450980392157, 0],
                [0.623529411764706, 0.435294117647059, 0],
                [0.627450980392157, 0.439215686274510, 0],
                [0.631372549019608, 0.447058823529412, 0.00784313725490196],
                [0.635294117647059, 0.454901960784314, 0.0235294117647059],
                [0.639215686274510, 0.462745098039216, 0.0352941176470588],
                [0.643137254901961, 0.466666666666667, 0.0470588235294118],
                [0.650980392156863, 0.474509803921569, 0.0588235294117647],
                [0.654901960784314, 0.482352941176471, 0.0705882352941177],
                [0.658823529411765, 0.490196078431373, 0.0823529411764706],
                [0.662745098039216, 0.494117647058824, 0.0941176470588235],
                [0.666666666666667, 0.501960784313726, 0.105882352941176],
                [0.670588235294118, 0.509803921568627, 0.117647058823529],
                [0.674509803921569, 0.517647058823530, 0.129411764705882],
                [0.678431372549020, 0.521568627450980, 0.141176470588235],
                [0.686274509803922, 0.529411764705882, 0.156862745098039],
                [0.690196078431373, 0.537254901960784, 0.168627450980392],
                [0.694117647058824, 0.545098039215686, 0.180392156862745],
                [0.694117647058824, 0.545098039215686, 0.180392156862745],
                [0.698039215686275, 0.549019607843137, 0.192156862745098],
                [0.701960784313725, 0.556862745098039, 0.203921568627451],
                [0.705882352941177, 0.564705882352941, 0.215686274509804],
                [0.709803921568628, 0.568627450980392, 0.227450980392157],
                [0.717647058823529, 0.576470588235294, 0.239215686274510],
                [0.721568627450980, 0.584313725490196, 0.250980392156863],
                [0.725490196078431, 0.592156862745098, 0.262745098039216],
                [0.729411764705882, 0.596078431372549, 0.274509803921569],
                [0.733333333333333, 0.603921568627451, 0.290196078431373],
                [0.737254901960784, 0.611764705882353, 0.301960784313725],
                [0.741176470588235, 0.619607843137255, 0.313725490196078],
                [0.745098039215686, 0.623529411764706, 0.325490196078431],
                [0.752941176470588, 0.631372549019608, 0.337254901960784],
                [0.756862745098039, 0.639215686274510, 0.349019607843137],
                [0.760784313725490, 0.647058823529412, 0.360784313725490],
                [0.764705882352941, 0.650980392156863, 0.372549019607843],
                [0.768627450980392, 0.658823529411765, 0.384313725490196],
                [0.768627450980392, 0.658823529411765, 0.384313725490196],
                [0.772549019607843, 0.666666666666667, 0.396078431372549],
                [0.776470588235294, 0.670588235294118, 0.407843137254902],
                [0.784313725490196, 0.678431372549020, 0.423529411764706],
                [0.788235294117647, 0.686274509803922, 0.435294117647059],
                [0.792156862745098, 0.694117647058824, 0.447058823529412],
                [0.796078431372549, 0.698039215686275, 0.458823529411765],
                [0.800000000000000, 0.705882352941177, 0.470588235294118],
                [0.803921568627451, 0.713725490196078, 0.482352941176471],
                [0.807843137254902, 0.721568627450980, 0.494117647058824],
                [0.811764705882353, 0.725490196078431, 0.505882352941176],
                [0.819607843137255, 0.733333333333333, 0.517647058823530],
                [0.823529411764706, 0.741176470588235, 0.529411764705882],
                [0.827450980392157, 0.749019607843137, 0.541176470588235],
                [0.831372549019608, 0.752941176470588, 0.552941176470588],
                [0.835294117647059, 0.760784313725490, 0.568627450980392],
                [0.839215686274510, 0.768627450980392, 0.580392156862745],
                [0.843137254901961, 0.772549019607843, 0.592156862745098],
                [0.843137254901961, 0.772549019607843, 0.592156862745098],
                [0.850980392156863, 0.780392156862745, 0.603921568627451],
                [0.854901960784314, 0.788235294117647, 0.615686274509804],
                [0.858823529411765, 0.796078431372549, 0.627450980392157],
                [0.862745098039216, 0.800000000000000, 0.639215686274510],
                [0.866666666666667, 0.807843137254902, 0.650980392156863],
                [0.870588235294118, 0.815686274509804, 0.662745098039216],
                [0.874509803921569, 0.823529411764706, 0.674509803921569],
                [0.878431372549020, 0.827450980392157, 0.686274509803922],
                [0.886274509803922, 0.835294117647059, 0.701960784313725],
                [0.890196078431373, 0.843137254901961, 0.713725490196078],
                [0.894117647058824, 0.850980392156863, 0.725490196078431],
                [0.898039215686275, 0.854901960784314, 0.737254901960784],
                [0.901960784313726, 0.862745098039216, 0.749019607843137],
                [0.905882352941177, 0.870588235294118, 0.760784313725490],
                [0.909803921568627, 0.874509803921569, 0.772549019607843],
                [0.917647058823529, 0.882352941176471, 0.784313725490196],
                [0.921568627450980, 0.890196078431373, 0.796078431372549],
                [0.921568627450980, 0.890196078431373, 0.796078431372549],
                [0.925490196078431, 0.898039215686275, 0.807843137254902],
                [0.929411764705882, 0.901960784313726, 0.819607843137255],
                [0.933333333333333, 0.909803921568627, 0.835294117647059],
                [0.937254901960784, 0.917647058823529, 0.847058823529412],
                [0.941176470588235, 0.925490196078431, 0.858823529411765],
                [0.945098039215686, 0.929411764705882, 0.870588235294118],
                [0.952941176470588, 0.937254901960784, 0.882352941176471],
                [0.956862745098039, 0.945098039215686, 0.894117647058824],
                [0.960784313725490, 0.952941176470588, 0.905882352941177],
                [0.964705882352941, 0.956862745098039, 0.917647058823529],
                [0.968627450980392, 0.964705882352941, 0.929411764705882],
                [0.972549019607843, 0.972549019607843, 0.941176470588235],
                [0.976470588235294, 0.976470588235294, 0.952941176470588],
                [0.980392156862745, 0.984313725490196, 0.964705882352941],
                [0.988235294117647, 0.992156862745098, 0.980392156862745],
                [0.992156862745098, 1, 0.992156862745098],
            ]
        )
