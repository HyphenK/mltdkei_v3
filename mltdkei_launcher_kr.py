# mltdkei Module #
import mltdkei_v40

IDB_name = 'mltdkei_idoldata_kr.sqlite'
MDB_name = 'mltdkei_songdata_kr.sqlite'
info_name = 'mltdkei_info_kr.txt'
SongDB_name = 'name_kr'

if __name__ == '__main__':
    mltdkei_v40.mltdkei_mainframe(IDB_name, MDB_name, info_name, SongDB_name)